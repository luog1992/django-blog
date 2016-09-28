import re

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from article.models import Blog, Tag, Category, Collection
from forms import BlogEditor, CategoryForm, TagForm, LoginForm



def tag_cloud(func):
    def wrapper(*args, **kwargs):
        tags = Tag.objects.get_valid_tags()
        cxt={'tag_cloud': tags}
        return func(cxt=cxt, *args, **kwargs)
    return wrapper


def request_splitter(request, *args, **kwargs):
    get_view = kwargs.pop('GET', None)
    post_view = kwargs.pop('POST', None)
    if request.method == 'GET' and get_view:
        return get_view(request, *args, **kwargs)
    elif request.method == 'POST' and post_view:
        return post_view(request, *args, **kwargs)
    raise Http404


def login(request):
    cxt = {}
    cxt.update(csrf(request))
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        next_page = request.POST.get('next', '/home/')
        if login_form.is_valid():
            data = login_form.cleaned_data
            username = data['username']
            password = data['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return redirect('%s' % next_page)
            else:
                login_form.add_error('username', 'Invalid user or password')
    else:
        login_form = LoginForm()
        next_page = request.GET.get('next', '/home/')
    cxt.update({'login_form': login_form, 'next': next_page})
    return render_to_response('registration/login.html', cxt)


def logout(request):
    auth.logout(request)
    return redirect('/home/')


def search(request, flag=None):
    if flag:
        if 'q' in request.GET:
            q = request.GET['q']
            if flag == 'categories':
                categories = Category.objects.filter(
                    name__icontains=q, valid=True)
                return render_to_response('category_list.html', {'categories': categories})
            if flag == 'tags':
                return redirect('/tags/')
    else:
        return Http404


@tag_cloud
def blogs(request, filter, name, cxt={}):
    if filter=='blog':
        all_blogs = Blog.objects.filter(valid=True)
    elif filter=='tag':
        tag = get_object_or_404(Tag, name=name)
        all_blogs = tag.valid_blogs()
    elif filter=='category':
        category = get_object_or_404(Category, name=name)
        all_blogs = category.get_valid_blogs()
    else:
        raise Http404
    paginator = Paginator(all_blogs, 2)
    page = request.GET.get('page')
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.paginator(paginator.num_pages)
    cxt.update({'blogs': blogs})
    return render_to_response('blog_list.html', cxt)


@tag_cloud
def blog_detail(request, id='0', cxt={}):
    try:
        blog = Blog.objects.get(id=int(id))
    except Blog.DoesNotExist:
        raise Http404
    cxt.update({'blog': blog, 'user': request.user})
    return render_to_response('blog_detail.html', cxt)


def blog_add(request):
    blog = Blog.objects.get_new_blog()
    return redirect('/blog/%s/modify/' % blog.id)


@tag_cloud
@login_required
def blog_edit_get(request, cxt={}, *args, **kwargs):
    assert request.method == 'GET'
    cxt.update(csrf(request))
    id = int(kwargs['id'])
    blog = Blog.objects.get(id=id)
    initial = {
        'title': blog.title,
        'category': blog.category.name,
        'tags': ' | '.join([tag.name for tag in blog.tags.all()]),
        'content': blog.content
    }
    blog_editor = BlogEditor(initial=initial)
    cxt.update({'blog': blog, 'blog_editor': blog_editor})
    return render_to_response('blog_edit.html', cxt)


@tag_cloud
@login_required
def blog_edit_post(request, cxt={}, *args, **kwargs):
    assert request.method == 'POST'
    cxt.update(csrf(request))
    id = int(kwargs['id'])
    blog = Blog.objects.get(id=id)
    blog_editor = BlogEditor(request.POST)
    cxt.update({'blog': blog, 'blog_editor': blog_editor})
    if blog_editor.is_valid():
        data = blog_editor.cleaned_data
        Blog.objects.save_blog(blog, data)
        return redirect('/blog/%s/edit/' % blog.id)
    else:
        return render_to_response('blog_edit.html', cxt)


@login_required
def blog_del(request, id='0'):
    Blog.objects.del_blog(int(id))
    return redirect('/home/')


@tag_cloud
def tags(request, cxt={}):
    tags = Tag.objects.all()
    tag_cat_keys = list(set([tag.name[0] for tag in tags]))
    tag_cats = []
    for tag_cat_key in tag_cat_keys:
        tag_cat_val = []
        for tag in tags:
            if tag.name[0] == tag_cat_key:
                tag_cat_val.append(tag)
        tag_cats.append(tag_cat_val)
    cxt.update({'tag_cats': tag_cats, 'user': request.user})
    return render_to_response('tag_list.html', cxt)


@login_required
def tag_add(request):
    untitle = Tag.objects.get_untitle()
    tag = Tag(name=untitle)
    tag.save()
    return redirect('/tag/%s/modify/' % tag.id)


@login_required
def tag_del(request, id='0'):
    Tag.objects.get(id=int(id)).delete()
    return redirect('/tags/')


@tag_cloud
@login_required
def tag_edit_get(request, id='0', cxt={}):
    assert request.method == 'GET'
    cxt.update(csrf(request))
    tag = Tag.objects.get(id=int(id))
    initial = {
        'name': tag.name,
        'color': tag.color
    }
    tag_form = TagForm(initial=initial)
    cxt.update({'tag_form': tag_form, 'tag': tag})
    return render_to_response('tag_edit.html', cxt)


@tag_cloud
@login_required
def tag_edit_post(request, id='0', cxt={}):
    assert request.method == 'POST'
    cxt.update(csrf(request))
    tag = Tag.objects.get(id=int(id))
    initial = {
        'name': tag.name,
        'color': tag.color
    }
    tag_form = TagForm(request.POST, initial=initial)
    cxt.update({'tag_form': tag_form, 'tag': tag})
    if tag_form.is_valid():
        data = tag_form.cleaned_data
        tag_name = data['name'].lower()
        if 'name' in tag_form.changed_data:
            if Tag.objects.filter(name=tag_name):
                tag_form.add_error('name', 'Duplicated Tag Name')
            else:
                Tag.objects.filter(id=int(id)).update(
                    name=tag_name,
                    color='#' + data['color'][-6:]
                )
        else:
            Tag.objects.filter(id=id).update(
                color='#' + data['color'][-6:]
            )
    return render_to_response('tag_edit.html', cxt)


@tag_cloud
def categories(request, cxt={}):
    categories = Category.objects.filter(valid=True)
    cxt.update({'categories': categories, 'user': request.user})
    return render_to_response('category_list.html', cxt)


@login_required
def category_add(request):
    untitle = Category.objects.get_untitle()
    category = Category(name=untitle)
    category.save()
    return redirect('/category/%s/modify/' % category.id)


@login_required
def category_del(request, id='0'):
    name_old = Category.objects.get(id=int(id)).name
    Category.objects.filter(id=int(id)).update(
        name=name_old + '_Old', valid=False)
    return redirect('/categories/')


@tag_cloud
@login_required
def cat_modify_get(request, id='0', cxt={}):
    assert request.method == 'GET'
    cxt.update(csrf(request))
    category = Category.objects.get(id=int(id))
    initial = {
        'name': category.name,
        'color': category.color,
        'public': category.public
    }
    category_form = CategoryForm(initial=initial)
    cxt.update({'category_form': category_form, 'category': category})
    return render_to_response('category_modify.html', cxt)


@tag_cloud
@login_required
def cat_modify_post(request, id='0', cxt={}):
    assert request.method == 'POST'
    cxt.update(csrf(request))
    category = Category.objects.get(id=int(id))
    initial = {
        'name': category.name,
        'color': category.color,
        'public': category.public
    }
    category_form = CategoryForm(request.POST, initial=initial)
    cxt.update({'category_form': category_form, 'category': category})
    if category_form.is_valid():
        data = category_form.cleaned_data
        category_name = data['name']
        if 'name' in category_form.changed_data:
            if Category.objects.filter(name=category_name):
                category_form.add_error('name', 'Duplicated Category Name')
            else:
                Category.objects.filter(id=int(id)).update(
                    name=data['name'],
                    color='#' + data['color'][-6:],
                    public=data['public']
                )
        else:
            Category.objects.filter(id=int(id)).update(
                color='#' + data['color'][-6:],
                public=data['public']
            )
    return render_to_response('category_modify.html', cxt)


@login_required
def cat_edit_blog_get(request, catid='0', blogid='0'):
    assert request.method == 'GET'
    cxt = {}
    cxt.update(csrf(request))
    category = Category.objects.get(id=int(catid))
    blog_ids = [blog.id for blog in category.blogs.all()]
    blogid = int(blogid)
    if blogid and blogid in blog_ids:
        blog = Blog.objects.get(id=blogid)
    else:
        blogs = category.get_valid_blogs()
        if blogs:
            blog = blogs[0]
        else:
            blog = Blog.objects.get_new_blog(catid=int(catid))

    blog_editor = BlogEditor(initial={
        'title': blog.title,
        'category': blog.category.name,
        'tags': ' | '.join([tag.name for tag in blog.tags.all()]),
        'content': blog.content
    })
    cxt.update({'category': category, 'blog': blog,
                'blog_editor': blog_editor})
    return render_to_response('category_edit.html', cxt)


@login_required
def cat_edit_blog_post(request, catid='0', blogid='0'):
    assert request.method == 'POST'
    blog = Blog.objects.get(id=int(blogid))
    blog_editor = BlogEditor(request.POST)
    if blog_editor.is_valid():
        data = blog_editor.cleaned_data
        Blog.objects.save_blog(blog, data)
    return redirect('/category/%s/edit/%s' % (catid, blogid))


@login_required
def cat_del_blog(request, catid='0', blogid='0'):
    Blog.objects.del_blog(int(blogid))
    return redirect('/category/%s/edit/0' % catid)


@login_required
def cat_add_blog(request, catid='0'):
    blog = Blog.objects.get_new_blog(catid=int(catid))
    return redirect('/category/%s/edit/%s' % (catid, blog.id))


def request(request):
    info = request.COOKIES
    # print '.... request.GET', request.GET
    # print '.... request.POST', request.POST
    # print '....', request.path
    # print '....', request.get_host()
    # print '....', request.get_full_path()
    # print '....', request.is_secure()
    # print '....', 'request.META'
    # print '........ HTTP_USER_AGENT', request.META['HTTP_USER_AGENT']
    # print '........ REMOTE_ADDR', request.META['REMOTE_ADDR']
    # for key in request.META:
    # print '........', key, request.META[key]
    return render_to_response('request.html', {'info': info})


def datatable(request):
    return render_to_response('datatable.html')

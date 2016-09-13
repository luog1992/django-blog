from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template.context_processors import csrf
from django.http import Http404
from article.models import Blog, Tag, Category, Collection
from forms import BlogEditor, CategoryForm, TagForm

import re
from functools import wraps


valid_tags = Tag.objects.get_valid_tags()
def tag_cloud(tags):
    def outer_wrapper(func):
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            return func(tag_cloud=tags, *args, **kwargs)
        return inner_wrapper
    return outer_wrapper


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


@tag_cloud(valid_tags)
def blogs(request, tag_cloud=None):
    blogs = Blog.objects.filter(valid=True)
    return render_to_response('blog_list.html', {'blogs': blogs, 'tag_cloud': tag_cloud})


@tag_cloud(valid_tags)
def blog_detail(request, id=0, tag_cloud=None):
    try:
        blog = Blog.objects.get(id=int(id))
    except Blog.DoesNotExist:
        raise Http404
    return render_to_response('blog_detail.html', {'blog': blog, 'tag_cloud': tag_cloud})


def blog_add(request, tag_cloud=None):
    blog = Blog.objects.get_new_blog()
    return redirect('/blog/%s/edit/' % blog.id)


@tag_cloud(valid_tags)
def blog_edit(request, id=0, tag_cloud=None):
    id = int(id)
    cxt = {}
    cxt.update(csrf(request))
    if request.method == 'POST':
        blog_editor = BlogEditor(request.POST)
        blog = Blog.objects.get(id=id)
        cxt.update({'blog': blog, 'blog_editor': blog_editor})
        if blog_editor.is_valid():
            data = blog_editor.cleaned_data
            Blog.objects.save_blog(blog, data)
            return redirect('/blog/%s/edit/' % blog.id)
    else:
        blog = Blog.objects.get(id=id)
        blog_editor = BlogEditor(initial={
            'title': blog.title,
            'category': blog.category.name,
            'tags': ' | '.join([tag.name for tag in blog.tags.all()]),
            'content': blog.content
        })
        cxt.update({'blog': blog, 'blog_editor': blog_editor})

    cxt.update({'tag_cloud': tag_cloud})
    return render_to_response('blog_edit.html', cxt)


def blog_del(request, id=0):
    Blog.objects.del_blog(id)
    return redirect('/home/')


@tag_cloud(valid_tags)
def tag_blogs(request, name, tag_cloud=None):
    try:
        tag = Tag.objects.filter(name=name)[0]
    except:
        raise Http404

    blogs = tag.blogs.filter(valid=True)
    return render_to_response('blog_list.html', {'blogs': blogs, 'tag_cloud': tag_cloud})


@tag_cloud(valid_tags)
def tags(request, tag_cloud=None):
    tags = Tag.objects.all()
    tag_cat_keys = list(set([tag.name[0] for tag in tags]))
    tag_cats = []
    for tag_cat_key in tag_cat_keys:
        tag_cat_val = []
        for tag in tags:
            if tag.name[0] == tag_cat_key:
                tag_cat_val.append(tag)
        tag_cats.append(tag_cat_val)

    return render_to_response('tag_list.html', {'tag_cats': tag_cats, 'tag_cloud': tag_cloud})


def tag_add(request):
    untitle = Tag.objects.get_untitle()
    tag = Tag(name=untitle)
    tag.save()
    return redirect('/tag/%s/edit/' % tag.id)


def tag_del(request, id):
    Tag.objects.get(id=int(id)).delete()
    return redirect('/tags/')


@tag_cloud(valid_tags)
def tag_edit(request, id, tag_cloud=None):
    id = int(id)
    cxt = {}
    cxt.update(csrf(request))
    tag = Tag.objects.get(id=id)
    initial = {
        'name': tag.name,
        'color': tag.color,
    }

    if request.method == 'POST':
        tag_form = TagForm(request.POST, initial=initial)
        if tag_form.is_valid():
            data = tag_form.cleaned_data
            tag_name = data['name'].lower()
            if tag_form.has_changed():
                if 'name' in tag_form.changed_data:
                    if Tag.objects.filter(name=tag_name):
                        tag_form.add_error('name', 'Duplicated Tag Name')
                    else:
                        Tag.objects.filter(id=id).update(
                            name=tag_name,
                            color=data['color'][-6:]
                        )
                else:
                    Tag.objects.filter(id=id).update(
                        color='#' + data['color'][-6:]
                    )
    else:
        tag_form = TagForm(initial=initial)

    cxt.update({'tag_form': tag_form, 'tag': tag, 'tag_cloud': tag_cloud})
    return render_to_response('tag_edit.html', cxt)


@tag_cloud(valid_tags)
def categories(request, tag_cloud=None):
    categories = Category.objects.filter(valid=True)
    return render_to_response('category_list.html', {'categories': categories, 'tag_cloud': tag_cloud})


def category_add(request, id=0):
    untitle = Category.objects.get_untitle()
    category = Category(name=untitle)
    category.save()
    return redirect('/category/%s/modify/' % category.id)


def category_del(request, id=0):
    id = int(id)
    name_old = Category.objects.get(id=id).name
    Category.objects.filter(id=int(id)).update(
        name=name_old + '_Old', valid=False)
    return redirect('/categories/')


@tag_cloud(valid_tags)
def category_modify(request, id=0, tag_cloud=None):
    id = int(id)
    cxt = {}
    cxt.update(csrf(request))
    category = Category.objects.get(id=id)
    initial = {
        'name': category.name,
        'color': category.color,
        'public': category.public
    }

    if request.method == 'POST':
        category_form = CategoryForm(request.POST, initial=initial)
        if category_form.is_valid():
            data = category_form.cleaned_data
            category_name = data['name']
            if category_form.has_changed():
                if 'name' in category_form.changed_data:
                    if Category.objects.filter(name=category_name):
                        category_form.add_error(
                            'name', 'Duplicated Category Name')
                    else:
                        Category.objects.filter(id=id).update(
                            name=data['name'],
                            color='#' + data['color'][-6:],
                            public=data['public']
                        )
                else:
                    Category.objects.filter(id=id).update(
                        color='#' + data['color'][-6:],
                        public=data['public']
                    )
    else:
        category_form = CategoryForm(initial=initial)

    cxt.update({'category_form': category_form, 'category': category, 'tag_cloud': tag_cloud})
    return render_to_response('category_modify.html', cxt)


def category_edit_blog(request, catid=0, blogid=0):
    catid = int(catid)
    blogid = int(blogid)
    cxt = {}
    cxt.update(csrf(request))
    if request.method == 'POST':
        blog_editor = BlogEditor(request.POST)
        blog = Blog.objects.get(id=blogid)
        cxt.update({'blog': blog, 'blog_editor': blog_editor})
        if blog_editor.is_valid():
            data = blog_editor.cleaned_data
            Blog.objects.save_blog(blog, data)
            return redirect('/category/%s/edit/%s' % (catid, blogid))
    else:
        category = Category.objects.get(id=catid)
        blog_ids = [cat.id for cat in category.blogs.all()]
        if blogid and blogid in blog_ids:
            blog = Blog.objects.get(id=blogid)
        else:
            blogs = category.get_valid_blogs()
            if blogs:
                blog = blogs[0]
            else:
                blog = Blog.objects.get_new_blog(catid=catid)

        blog_editor = BlogEditor(initial={
            'title': blog.title,
            'category': blog.category.name,
            'tags': ' | '.join([tag.name for tag in blog.tags.all()]),
            'content': blog.content
        })
        cxt.update({'category': category, 'blog': blog,
                    'blog_editor': blog_editor})
        return render_to_response('category_edit.html', cxt)


def category_del_blog(request, catid=0, blogid=0):
    Blog.objects.del_blog(blogid)
    return redirect('/category/%s/edit/0' % catid)


def category_add_blog(request, catid=0):
    blog = Blog.objects.get_new_blog(catid=int(catid))
    return redirect('/category/%s/edit/%s' % (catid, blog.id))


def request(request):
    print '.... request.GET', request.GET
    print '.... request.POST', request.POST
    print '....', request.path
    print '....', request.get_host()
    print '....', request.get_full_path()
    print '....', request.is_secure()
    print '....', 'request.META'
    print '........ HTTP_USER_AGENT', request.META['HTTP_USER_AGENT']
    print '........ REMOTE_ADDR', request.META['REMOTE_ADDR']
    # for key in request.META:
    # print '........', key, request.META[key]


def datatable(request):
    return render_to_response('datatable.html')

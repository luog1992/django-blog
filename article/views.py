from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template.context_processors import csrf
from django.http import Http404
from article.models import Blog, Tag, Category, Collection
from forms import BlogEditor, CategoryForm, TagForm
from utils import Constant, Tools
import random
import re


def search(request, flag=None):
    if flag:
        if 'q' in request.GET:
            q = request.GET['q']
            if flag == 'categories':
                categories = Category.objects.filter(name__icontains=q, valid=True)
                return render_to_response('category_list.html', {'categories': categories})
            if flag == 'tags':
                return redirect('/tags/')
    else:
        return Http404




def get_new_blog(catid=0, colid=0):
    cxt = {}
    cxt.update(csrf(request))
    if catid:
        category = Category.objects.get(id=catid)
    else:
        try:
            category = Category.objects.get(name='Default')
        except Category.DoesNotExist:
            category = Category(name='Default')
            category.save()
            category = Category.objects.get(name='Default')

    blog = Blog(category=category)

    if colid:
        collection = Collection.objects.get(id=colid)
        blog.collections.add(collection)

    blog.save()
    return blog


def save_blog(blog, blog_editor):
    data = blog_editor.cleaned_data
    blog.title = data['title']
    blog.category = Category.objects.get(name=data['category'])
    blog.content = data['content']
    blog.update_summary()
    tags_raw = list(set(filter(lambda item: item != '', [tag.strip(
        ' ,;').lower() for tag in (data['tags']).split('|') if tag])))
    if tags_raw:
        tags_all = [tag.name for tag in Tag.objects.all()]
        tags_new = list(set(tags_raw) - set(tags_all))
        if tags_new:
            for tag in tags_new:
                new_tag = Tag(
                    name=tag, color=random.choice(Constant.TAGCOLORS))
                new_tag.save()
        blog.tags.clear()
        for tag_name in tags_raw:
            blog.tags.add(Tag.objects.get(name=tag_name))
    else:
        blog.tags.clear()
    blog.save()


def del_blog(id=0):
    id = int(id)
    Blog.objects.filter(id=id).update(trash=True)

# -----------------------------------------------------------------------------------------

def blogs(request):
    blogs = Blog.objects.filter(trash=False)
    tag_cloud = Tag.objects.get_valid_tags()
    return render_to_response('blog_list.html', {'blogs': blogs, 'tag_cloud': tag_cloud})


def blog_detail(request, id=0):
    id = int(id)
    try:
        blog = Blog.objects.get(id=id)
    except Blog.DoesNotExist:
        raise Http404
    tag_cloud = Tag.objects.get_valid_tags()
    return render_to_response('blog_detail.html', {'blog': blog, 'tag_cloud': tag_cloud})


def blog_add(request):
    blog = get_new_blog()
    return redirect('/blog/%s/edit/' % blog.id)


def blog_edit(request, id=0):
    id = int(id)
    cxt = {}
    cxt.update(csrf(request))
    if request.method == 'POST':
        blog_editor = BlogEditor(request.POST)
        blog = Blog.objects.get(id=id)
        cxt.update({'blog': blog, 'blog_editor': blog_editor})
        if blog_editor.is_valid():
            save_blog(blog, blog_editor)
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

    tag_cloud = Tag.objects.get_valid_tags()
    cxt.update({'tag_cloud': tag_cloud})
    return render_to_response('blog_edit.html', cxt)


def blog_del(request, id=0):
    del_blog(id)
    return redirect('/home/')


def tag_blogs(request, name):
    try:
        tag = Tag.objects.filter(name=name)[0]
    except:
        raise Http404

    blogs = tag.blogs.filter(trash=False)
    tag_cloud = Tag.objects.get_valid_tags()
    return render_to_response('blog_list.html', {'blogs': blogs, 'tag_cloud': tag_cloud})


def tags(request):
    tags = Tag.objects.all()
    tag_cat_keys = list(set([tag.name[0] for tag in tags]))
    tag_cats = []
    for tag_cat_key in tag_cat_keys:
        tag_cat_val = []
        for tag in tags:
            if tag.name[0] == tag_cat_key:
                tag_cat_val.append(tag)
        tag_cats.append(tag_cat_val)

    tag_cloud = Tag.objects.get_valid_tags()
    return render_to_response('tag_list.html', {'tag_cats': tag_cats, 'tag_cloud': tag_cloud})


def tag_add(request):
    untitle = Tag.objects.get_untitle()
    tag = Tag(name=untitle)
    tag.save()
    return redirect('/tag/%s/edit/' % tag.id)


def tag_del(request, id):
    Tag.objects.get(id=int(id)).delete()
    return redirect('/tags/')


def tag_edit(request, id):
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

    cxt.update({'tag_form': tag_form, 'tag': tag})
    return render_to_response('tag_edit.html', cxt)


def categories(request):
    categories = Category.objects.filter(valid=True)
    return render_to_response('category_list.html', {'categories': categories})


def category_add(request, id=0):
    untitle = Category.objects.get_untitle()
    category = Category(name=untitle)
    category.save()
    return redirect('/category/%s/modify/' % category.id)


def category_del(request, id=0):
    id = int(id)
    name_old = Category.objects.get(id=id).name
    Category.objects.filter(id=int(id)).update(name=name_old+'_Old', valid=False)
    return redirect('/categories/')


def category_modify(request, id=0):
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
                        category_form.add_error('name', 'Duplicated Category Name')
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

    cxt.update({'category_form': category_form, 'category': category})
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
            save_blog(blog, blog_editor)
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
                blog = get_new_blog(catid=catid)

        blog_editor = BlogEditor(initial={
            'title': blog.title,
            'category': blog.category.name,
            'tags': ' | '.join([tag.name for tag in blog.tags.all()]),
            'content': blog.content
        })
        cxt.update({'category': category, 'blog': blog, 'blog_editor': blog_editor})
        return render_to_response('category_edit.html', cxt)


def category_del_blog(request, catid=0, blogid=0):
    del_blog(blogid)
    return redirect('/category/%s/edit/0' % catid)


def category_add_blog(request, catid=0):
    blog = get_new_blog(catid=catid)
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

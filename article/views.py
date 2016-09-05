from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template.context_processors import csrf
from django.http import Http404
from article.models import Blog, Tag, Category, Collection
from forms import BlogEditor
from utils import Constant, Tools
import random
import re


def search(request):
    if 'q' in request.GET:
        print request.GET['q']


def blogs(request):
    blogs = Blog.objects.filter(valid=True)
    tag_cloud = Tag.objects.all().order_by('color')
    return render_to_response('blog_list.html', {'blogs': blogs, 'tag_cloud': tag_cloud})


def blog_detail(request, id=0):
    id = int(id)
    try:
        blog = Blog.objects.get(id=id)
    except Blog.DoesNotExist:
        raise Http404
    tag_cloud = Tag.objects.all().order_by('color')
    return render_to_response('blog_detail.html', {'blog': blog, 'tag_cloud': tag_cloud})


def blog_add(request):
    print '....blog add', request.method
    cxt = {}
    cxt.update(csrf(request))
    try:
        default_cat = Category.objects.get(name='Default')
    except Category.DoesNotExist:
        default_cat = Category(name='Default')
        default_cat.save()
        default_cat = Category.objects.get(name='Default')
    blog = Blog(category=default_cat)
    blog.save()
    return redirect('/blog/%s/edit/' % blog.id)


def blog_edit(request, id=0):
    id = int(id)
    cxt = {}
    cxt.update(csrf(request))
    print '....blog edit', request.method
    if request.method == 'POST':
        print '........blog save'
        print '........request.get_full_path', request.get_full_path()
        blog_editor = BlogEditor(request.POST)
        blog = Blog.objects.get(id=id)
        cxt.update({'blog': blog, 'blog_editor': blog_editor})
        if blog_editor.is_valid():
            data = blog_editor.cleaned_data
            blog.valid = True
            blog.title = data['title']
            blog.category = Category.objects.get(name=data['category'])
            blog.content = data['content']
            blog.summary = Tools.get_summary(data['content'])
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

    tag_cloud = Tag.objects.all().order_by('color')
    cxt.update({'tag_cloud': tag_cloud})
    return render_to_response('blog_edit.html', cxt)


def blog_del(request, id=0):
    print '....blog del'
    id = int(id)
    Blog.objects.filter(id=id).update(valid=False)
    return redirect('/home/')


def tag_blogs(request, name):
    try:
        tag = Tag.objects.filter(name=name)[0]
    except:
        raise Http404

    blogs = tag.blogs.all()
    tag_cloud = Tag.objects.all().order_by('color')
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

    tag_cloud = Tag.objects.all().order_by('color')
    return render_to_response('tag_list.html', {'tag_cats': tag_cats, 'tag_cloud': tag_cloud})


def tag_edit(request, id):
    id = int(id)
    cxt = {}
    cxt.update(csrf(request))
    if request.method == 'POST':
        print '....tag_modify', request.POST.get('content')
        Tag.objects.filter(id=id).update(
            name=request.POST.get('name'),
            color='#' + request.POST.get('color')[-6:],
        )
    tag = Tag.objects.get(id=id)
    cxt.update({'tag': tag})
    return render_to_response('tag_edit.html', cxt)


def categories(request):
    categories = Category.objects.all()
    return render_to_response('category_list.html', {'categories': categories})


def category_detail(request, id):
    id = int(id)
    cxt = {}
    cxt.update(csrf(request))
    category = Category.objects.get(id=id)
    blog = category.get_valid_blogs()[0]
    blog_editor = BlogEditor(initial={
        'title': blog.title,
        'category': blog.category.name,
        'tags': ' | '.join([tag.name for tag in blog.tags.all()]),
        'content': blog.content
    })
    cxt.update({'category': category, 'blog': blog, 'blog_editor': blog_editor})
    return render_to_response('category_detail.html', cxt)


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

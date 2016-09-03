from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template.context_processors import csrf
from django.http import Http404
from article.models import Blog, Tag, Category
from forms import BlogEditor
import re


# def home(request):
#   post_list = Blog.objects.all()
#   return render_to_response('home.html', {'post_list': post_list})

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
    return blog_edit(request, id=blog.id)


def blog_edit(request, id=0):
    id = int(id)
    cxt = {}
    cxt.update(csrf(request))
    print '....blog edit', request.method
    if request.method == 'POST':
        print '........blog saved'
        blog = Blog.objects.get(id=id)
        blog.valid = True
        blog.title = request.POST.get('title')
        blog.category = Category.objects.get(name=request.POST.get('category'))
        blog.content = request.POST.get('content')
        patt_sum = re.compile(r'@sum(.*?)@endsum', re.S)
        summary = patt_sum.findall(blog.content)
        if summary:
            blog.summary = summary[0].strip('\n <br>')
        tags_raw = filter(lambda item: item != '', [tag.strip(
            ' ,;').lower() for tag in (request.POST.get('tags')).split('|') if tag])
        if tags_raw:
            tags_all = [tag.name for tag in Tag.objects.all()]
            tags_new = list(set(tags_raw) - set(tags_all))
            if tags_new:
                Tag.objects.bulk_create([Tag(name=tag) for tag in tags_new])
            blog.tags.clear()
            for tag_name in tags_raw:
                blog.tags.add(Tag.objects.get(name=tag_name))
        blog.save()

    try:
        blog = Blog.objects.get(id=id)
    except Blog.DoesNotExist:
        raise Http404

    blog_editor = BlogEditor(initial={
        'title': blog.title,
        'category': blog.category.name,
        'tags': ' | '.join([tag.name for tag in blog.tags.all()]),
        'content': blog.content
    })
    tag_cloud = Tag.objects.all().order_by('color')
    cxt.update({'blog': blog, 'tag_cloud': tag_cloud, 'blog_editor': blog_editor})
    return render_to_response('blog_edit.html', cxt)


def blog_del(request, id=0):
    print '....blog del'
    id = int(id)
    Blog.objects.filter(id=id).update(valid=False)
    return redirect('/home')

def blog_tags(request):
    tags = Tag.objects.all()
    tag_cat_keys =list(set([tag.name[0] for tag in tags]))
    tag_cats = []
    for tag_cat_key in tag_cat_keys:
        tag_cat_val = []
        for tag in tags:
            if tag.name[0] == tag_cat_key:
                tag_cat_val.append(tag)
        tag_cats.append(tag_cat_val)

    tag_cloud = Tag.objects.all().order_by('color')
    return render_to_response('blog_tags.html', \
        {'tag_cats': tag_cats, 'tag_cloud': tag_cloud})

def tag_blogs(request, name):
    try:
        tag = Tag.objects.filter(name=name)[0]
    except:
        raise Http404

    blogs = tag.blogs.all()
    tag_cloud = Tag.objects.all().order_by('color')
    return render_to_response('blog_list.html', {'blogs': blogs, 'tag_cloud': tag_cloud})

def tag_modify(request, id):
    id = int(id)
    cxt = {}
    cxt.update(csrf(request))
    if request.method == 'POST':
        Tag.objects.filter(id=id).update(
            name=request.POST.get('name'),
            color='#' + request.POST.get('color'),
        )
    tag = Tag.objects.get(id=id)
    cxt.update({'tag': tag})
    return render_to_response('tag_modify.html', cxt)

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

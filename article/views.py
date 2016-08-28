from django.shortcuts import render_to_response
from django.template.context_processors import csrf
from django.http import Http404
from article.models import Blog, Tag, Category
from forms import BlogEditor


# def home(request):
# 	post_list = Blog.objects.all()
# 	return render_to_response('home.html', {'post_list': post_list})

def search(request):
    if 'q' in request.GET:
        print request.GET['q']


def blogs(request):
    blogs = Blog.objects.all()
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


def blog_edit(request, id=0):
    cxt = {}
    cxt.update(csrf(request))
    print '....Request.Method:', request.method
    if request.method == 'POST':
        print '....', request.POST.get('title')
        print '....', request.POST.get('tags')
        print '....', request.POST.get('content')

    id = int(id)
    try:
        blog = Blog.objects.get(id=id)
    except Blog.DoesNotExist:
        raise Http404

    blog_editor = BlogEditor(initial={
    	'title': blog.title,
    	'tags': ', '.join([tag.name for tag in blog.tags.all()]),
    	'content': blog.content
    })
    tag_cloud = Tag.objects.all().order_by('color')
    cxt.update({'blog': blog, 'tag_cloud': tag_cloud,
                'blog_editor': blog_editor})
    return render_to_response('blog_edit_test.html', cxt)


def tag_blogs(request, name):
    try:
        tag = Tag.objects.filter(name=name)[0]
    except:
        raise Http404
    print tag
    blogs = tag.blogs.all()
    tag_cloud = Tag.objects.all().order_by('color')
    return render_to_response('blog_list.html', {'blogs': blogs, 'tag_cloud': tag_cloud})


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

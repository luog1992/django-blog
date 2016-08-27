from django.shortcuts import render_to_response
from django.http import Http404
from article.models import Blog, Tag, Category


# def home(request):
# 	post_list = Blog.objects.all()
# 	return render_to_response('home.html', {'post_list': post_list})

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

def tag_blogs(request, name):
	try:
		tag = Tag.objects.filter(name=name)[0]
	except:
		raise Http404
	print tag
	blogs = tag.blogs.all()
	tag_cloud = Tag.objects.all().order_by('color')
	return render_to_response('blog_list.html', {'blogs': blogs, 'tag_cloud': tag_cloud})
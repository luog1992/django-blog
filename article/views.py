from django.shortcuts import render_to_response

from article.models import Article

def home(request):
	post_list = Article.objects.all()
	return render_to_response('home.html', {'post_list': post_list})

def detail(request, post_num):
	post_list = Article.objects.all()[:post_num]
	return render_to_response('articles.html', {'post_list': post_list})


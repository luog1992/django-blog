from django.shortcuts import render_to_response
from django.http import Http404
from article.models import Article

def home(request):
	post_list = Article.objects.all()
	return render_to_response('home.html', {'post_list': post_list})

def article_list(request, post_num=0):
	try:
		if post_num == 0:
			post_list = Article.objects.all()
		elif post_num > 0:
			post_list = Article.objects.all()[:post_num]
	except Article.DoesNotExist:
		raise Http404
	return render_to_response('article_list.html', {'post_list': post_list})

def article(request, id):
	try:
		post = Article.objects.get(id=str(id))
	except Article.DoesNotExist:
		raise Http404
	# return render_to_response('arti')




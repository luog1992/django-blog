from django.shortcuts import render_to_response
from django.http import Http404
from article.models import Article

def articles(request):
	post_list = Article.objects.all()
	return render_to_response('article_list.html', {'post_list': post_list})

def article(request, id):
	try:
		post = Article.objects.get(id=str(id))
	except Article.DoesNotExist:
		raise Http404
	return render_to_response('article.html', {'post': post})




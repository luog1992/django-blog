from django.shortcuts import render_to_response
from django.http import Http404
from article.models import Article


def home(request):
	post_list = Article.objects.all()
	return render_to_response('home.html', {'post_list': post_list})

def article(request, id):
	try:
		post = Article.objects.get(id=id)
	except Article.DoesNotExist:
		raise Http404
	return render_to_response('article.html', {'post': post})



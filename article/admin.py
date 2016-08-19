from django.contrib import admin
from article.models import Article
from django import forms
from pagedown.widgets import AdminPagedownWidget


class ArticleForm(forms.ModelForm):
	content = forms.CharField(widget=AdminPagedownWidget())
	class Meta:
		model = Article
		fields = '__all__'


class ArticleAdmin(admin.ModelAdmin):
	form = ArticleForm
	list_display  = ('title', 'category', 'date_time')
	search_fields = ('title', 'category')
	list_filter   = ('category', 'date_time')
	ordering      = ('-date_time', 'title')
	fields        = ('title', 'category', 'content')


# Register your models here
admin.site.register(Article, ArticleAdmin)
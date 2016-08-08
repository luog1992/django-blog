from django.contrib import admin
from article.models import Article

class ArticleAdmin(admin.ModelAdmin):
	list_display  = ('title', 'category', 'date_time')
	search_fields = ('title', 'category')
	list_filter   = ('category', 'date_time')
	ordering      = ('-date_time', 'title')
	fields        = ('title', 'category', 'content')


# Register your models here
admin.site.register(Article, ArticleAdmin)
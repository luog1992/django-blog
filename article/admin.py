from django.contrib import admin
from article.models import Article, Tag, Category


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date_time', 'summary')
    search_fields = ('title', 'category', 'tags')
    list_filter = ('date_time', 'category', 'tags')
    ordering = ('category', '-date_time', 'title')
    fields = ('title', 'tags', 'category', 'summary', 'content')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    search_fields = ('name', 'color')
    ordering = ('name', 'color')
    fields = ('name', 'color')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
    fields = ('name',)


# Register your models here
admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)

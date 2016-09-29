from django.contrib import admin
# because we used django as the broker, so the queue is stored in django database. So we can review the queue in django admin
from kombu.transport.django import models as kombu_models

from article.models import Blog, Tag, Category, Collection


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'public', 'valid', 'category', 'date_time', 'summary')
    search_fields = ('title', 'category', 'tags')
    list_filter = ('date_time', 'category', 'tags', 'public', 'valid')
    ordering = ('-valid', 'category', '-date_time', 'title')
    fields = ('title', 'public', 'tags', 'category', 'summary', 'content')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    search_fields = ('name', 'color')
    ordering = ('name', 'color')
    fields = ('name', 'color')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'public', 'valid', 'color')
    search_fields = ('name', 'color')
    ordering = ('-valid', 'name', 'public', 'color')
    fields = ('name', 'public', 'valid', 'color')

class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    search_fields = ('name', 'color')
    ordering = ('name', 'color')
    fields = ('name', 'color')

# Register your models here
admin.site.register(Blog, BlogAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(kombu_models.Message)

import re
import math
import random
from django.db import models
from django.core.urlresolvers import reverse

from utils import Constant


# class NewNameManager(models.Manager):
def get_untitle(aManager):
    patt = re.compile(r'untitle(\d{1,3})', re.I)
    nums = patt.findall(
        ','.join([cat.name for cat in aManager.filter(name__icontains='untitle')]))
    if nums:
        nums = map(int, nums)
        nums.sort()
        result = 'Untitle' + str(nums[-1] + 1)
    else:
        result = 'Untitle1'
    return result


class TagManager(models.Manager):

    def get_valid_tags(self):
        return [tag for tag in self.all() if tag.blog_nums() > 0]

    def get_untitle(self):
        return get_untitle(self)


class Tag(models.Model):
    name = models.CharField(verbose_name='Tag', max_length=20, unique=True)
    color = models.CharField(verbose_name='Color', max_length=20, default='#99CC99')
    objects = TagManager()

    def valid_blogs(self):
        return self.blogs.filter(valid=True)

    def blog_nums(self):
        return self.valid_blogs().count()

    def font_size(self):
        return 0.8 + (math.log10(self.blogs.count()))/10

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['color']


class CategoryManager(models.Manager):

    def get_untitle(self):
        return get_untitle(self)

    def get_valid_categories(self):
        return self.filter(valid=True).all()


class Category(models.Model):
    name = models.CharField(verbose_name='Category', max_length=50, unique=True)
    color = models.CharField(verbose_name='Color', max_length=20, default='#99CC99')
    public = models.BooleanField(verbose_name='Public', default=True)
    valid = models.BooleanField(verbose_name='Valid', default=True)
    objects = CategoryManager()

    def blog_nums(self):
        return self.blogs.filter(valid=True).count()

    def get_valid_blogs(self):
        return self.blogs.filter(valid=True).order_by('title')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Collection(models.Model):
    name = models.CharField(verbose_name='Collection', max_length=100, unique=True)
    color = models.CharField(verbose_name='Color', max_length=20, default='#99CC99')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class BlogManager(models.Manager):

    def get_new_blog(self, catid=0, colid=0):
        if catid:
            category = Category.objects.get(id=catid)
        else:
            try:
                category = Category.objects.get(name='Default')
            except Category.DoesNotExist:
                category = Category(name='Default')
                category.save()
                category = Category.objects.get(name='Default')
                
        blog = Blog(category=category)
        if colid:
            collection = Collection.objects.get(id=colid)
            blog.collections.add(collection)

        blog.save()
        return blog

    def save_blog(self, blog, data):
        blog.title = data['title']
        blog.category = Category.objects.get(name=data['category'])
        blog.content = data['content']
        blog.get_summary()
        tags_raw = list(set(filter(lambda item: item != '', [tag.strip(
            ' ,;').lower() for tag in (data['tags']).split('|') if tag])))
        if tags_raw:
            tags_all = [tag.name for tag in Tag.objects.all()]
            tags_new = list(set(tags_raw) - set(tags_all))
            if tags_new:
                for tag in tags_new:
                    new_tag = Tag(
                        name=tag, color=random.choice(Constant.TAGCOLORS))
                    new_tag.save()
            blog.tags.clear()
            for tag_name in tags_raw:
                blog.tags.add(Tag.objects.get(name=tag_name))
        else:
            blog.tags.clear()
        blog.save()

    def del_blog(self, id):
        Blog.objects.filter(id=int(id)).update(valid=False)


class Blog(models.Model):
    default_content = '@sum<br>Summary your blog here...<br>@endsum'
    title = models.CharField(verbose_name='Title', max_length=100, null=False, default='Untitle')
    public = models.BooleanField(verbose_name='Public', default=True)
    valid = models.BooleanField(verbose_name='Valid', default=True)
    date_time = models.DateField( verbose_name='Creation Date', auto_now_add=True)
    category = models.ForeignKey( Category, related_name='blogs', default=None, null=False)
    collections = models.ManyToManyField(Collection, related_name='blogs')
    tags = models.ManyToManyField(Tag, related_name='blogs')
    summary = models.TextField( verbose_name='Summary', max_length=1000, blank=True, null=True)
    content = models.TextField(verbose_name='Content', default=default_content)
    objects = BlogManager()

    def get_summary(self):
        patt_sum = re.compile(r'@sum(.*?)@endsum', re.S)
        summary = patt_sum.findall(self.content)
        if summary:
            summary = re.findall(r'>(.+?)<', summary[0])
            if summary:
                self.summary = summary[0]
            else:
                self.summary = self.content[:500] + '...'
        else:
            self.summary = self.content[:500] + '...'

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['category', 'title']

from django.db import models
from django.core.urlresolvers import reverse


class Tag(models.Model):
    name = models.CharField(verbose_name='Tag', max_length=20, unique=True)
    color = models.CharField(verbose_name='Color', max_length=20, default='#99CC99')

    def blog_nums(self):
        return self.blogs.count()

    def font_size(self):
        return 0.6 + (self.blogs.count()) / 5.0

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Category(models.Model):
    name = models.CharField(verbose_name='Category', max_length=20, unique=True)
    color = models.CharField(verbose_name='Color', max_length=20, default='#99CC99')

    def get_valid_blogs(self):
        return self.blogs.filter(valid=True, trash=False).order_by('title')

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


class Blog(models.Model):
    default_content = '@sum<br><br>Summary your blog here...<br><br>@endsum'
    title = models.CharField(verbose_name='Title', max_length=100, null=False, default='Untitle')
    public = models.BooleanField(verbose_name='Public', default=True)
    valid = models.BooleanField(verbose_name='Valid', default=False)
    trash = models.BooleanField(verbose_name='Trash', default=False)
    date_time = models.DateField(verbose_name='Creation Date', auto_now_add=True)
    category = models.ForeignKey(Category, related_name='blogs', default=None, null=False)
    collections = models.ManyToManyField(Collection, related_name='blogs', default=None, null=True)
    tags = models.ManyToManyField(Tag, related_name='blogs')
    summary = models.TextField(verbose_name='Summary', max_length=1000, blank=True, null=True)
    content = models.TextField(verbose_name='Content', default=default_content)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-date_time']

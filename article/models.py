from django.db import models
from django.core.urlresolvers import reverse


class Tag(models.Model):
    name = models.CharField(verbose_name='Tag', max_length=20)
    color = models.CharField(verbose_name='Color',
                             max_length=20, default='transparent')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Article(models.Model):
    title = models.CharField(verbose_name='Title', max_length=100)
    tags = models.ManyToManyField(Tag)
    date_time = models.DateField(
        verbose_name='Creation Date', auto_now_add=True)
    summary = models.TextField(
        verbose_name='Summary', max_length=1000, blank=True, null=True)
    content = models.TextField(verbose_name='Content', blank=True, null=True)

    def get_absolute_url(self):
        path = reverse('article', kwargs={'id': self.id})
        return "http://127.0.0.1:8000%s" % path

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-date_time']


class Category(models.Model):
    name = models.CharField(verbose_name='Category', max_length=20)
    color = models.CharField(verbose_name='Color',
                             max_length=20,  default='transparent')
    articles = models.ManyToManyField(Article)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

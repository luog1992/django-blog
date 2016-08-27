from django.db import models
from django.core.urlresolvers import reverse


class Tag(models.Model):
    name = models.CharField(verbose_name='Tag', max_length=20)
    color = models.CharField(verbose_name='Color', max_length=20, default='#BFE37C')

    def count(self):
        return 0.8+(self.blogs.count())/5.0

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Category(models.Model):
    name = models.CharField(verbose_name='Category', max_length=20)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Blog(models.Model):
    title = models.CharField(verbose_name='Title', max_length=100)
    date_time = models.DateField(verbose_name='Creation Date', auto_now_add=True)
    category = models.ForeignKey(Category, related_name='blogs', default=None, null=True)
    tags = models.ManyToManyField(Tag, related_name='blogs')
    summary = models.TextField(verbose_name='Summary', max_length=1000, blank=True, null=True)
    content = models.TextField(verbose_name='Content', default='')

    def get_absolute_url(self):
        path = reverse('article', kwargs={'id': self.id})
        return "http://127.0.0.1:8000%s" % path

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-date_time']

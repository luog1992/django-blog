from django.db import models
from django.core.urlresolvers import reverse

class Article(models.Model):
    title = models.CharField(verbose_name='Title', max_length=100)
    category = models.CharField(
        verbose_name='Category', max_length=50, blank=True)
    date_time = models.DateField(verbose_name='Creation Date', auto_now_add=True)
    content = models.TextField(verbose_name='Content', blank=True, null=True)

    def get_absolute_url(self):
        path = reverse('article', kwargs={'id':self.id})
        return "http://127.0.0.1:8000%s" % path

    def __unicode__(self):
        return self.title

    class Meta:
        ordering=['-date_time']

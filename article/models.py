import re
from django.db import models
from django.core.urlresolvers import reverse


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

    def blog_nums(self):
        return self.blogs.filter(trash=False).count()

    def font_size(self):
        return 0.6 + (self.blogs.count()) / 5.0

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
    name = models.CharField(verbose_name='Category', max_length=20, unique=True)
    color = models.CharField(verbose_name='Color', max_length=20, default='#99CC99')
    public = models.BooleanField(verbose_name='Public', default=True)
    valid = models.BooleanField(verbose_name='Valid', default=True)
    objects = CategoryManager()

    def blog_nums(self):
        return self.blogs.filter(trash=False).count()

    def get_valid_blogs(self):
        return self.blogs.filter(trash=False).order_by('title')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Collection(models.Model):
    name = models.CharField(verbose_name='Collection',
                            max_length=100, unique=True)
    color = models.CharField(verbose_name='Color',
                             max_length=20, default='#99CC99')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Blog(models.Model):
    default_content = '@sum<br><br>Summary your blog here...<br><br>@endsum'
    title = models.CharField(verbose_name='Title',
                             max_length=100, null=False, default='Untitle')
    public = models.BooleanField(verbose_name='Public', default=True)
    trash = models.BooleanField(verbose_name='Trash', default=False)
    date_time = models.DateField(
        verbose_name='Creation Date', auto_now_add=True)
    category = models.ForeignKey(
        Category, related_name='blogs', default=None, null=False)
    collections = models.ManyToManyField(Collection, related_name='blogs')
    tags = models.ManyToManyField(Tag, related_name='blogs')
    summary = models.TextField(
        verbose_name='Summary', max_length=1000, blank=True, null=True)
    content = models.TextField(verbose_name='Content', default=default_content)

    def update_summary(self):
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

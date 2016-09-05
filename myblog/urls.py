from django.conf.urls import patterns, url, include
from django.views.generic import RedirectView
from django.contrib import admin
admin.autodiscover()


# urlpatterns = [
#     url(r'^admin/', include(admin.site.urls)),
# ]

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^summernote/', include('django_summernote.urls')),
)

urlpatterns += patterns('article.views',
	url(r'^request/$', 'request'),
	url(r'^search/$', 'search', name='search'),
	url(r'^home/$', 'blogs', name='home'),
	url(r'^blogs/$', 'blogs', name='blogs'),
	url(r'^blog/add/$', 'blog_add', name='blog_add'),
	url(r'^blog/(?P<id>\d{1,3})/detail/$', 'blog_detail', name='blog_detail'),
	url(r'^blog/(?P<id>\d{1,3})/edit/$', 'blog_edit', name='blog_edit'),
	url(r'^blog/(?P<id>\d{1,3})/delete/$', 'blog_del', name='blog_del'),

	url(r'^tags/$', 'tags', name='tags'),
	url(r'^tag/(?P<id>\d{1,3})/edit/$', 'tag_edit', name='tag_edit'),
	url(r'^tag/(?P<name>\w{1,20})/blogs/', 'tag_blogs', name='tag_blogs'),

	url(r'^categories/$', 'categories', name='categories'),
	url(r'^category/(?P<id>\d{1,3})/detail/$', 'category_detail', name='category_detail'),
)
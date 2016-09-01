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
	url(r'^blog/(?P<id>\d{1,3})/detail$', 'blog_detail', name='blog_detail'),
	url(r'^blog/add$', 'blog_add', name='blog_add'),
	url(r'^blog/(?P<id>\d{1,3})/edit/$', 'blog_edit', name='blog_edit'),
	url(r'^blog/(?P<id>\d{1,3})/delete/$', 'blog_del', name='blog_del'),
	url(r'^tag/(?P<name>\w{1,20})', 'tag_blogs', name='tag_blogs'),
)
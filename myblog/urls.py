from django.conf.urls import patterns, url, include
from django.views.generic import RedirectView
from django.contrib import admin
admin.autodiscover()


# urlpatterns = [
#     url(r'^admin/', include(admin.site.urls)),
# ]

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('article.views',
	url(r'^request/$', 'request'),
	url(r'^search/$', 'search', name='search'),
	url(r'^home/$', 'blogs', name='home'),
	url(r'^blogs/$', 'blogs', name='blogs'),
	url(r'^blog/(?P<id>\d{1,3})/detail$', 'blog_detail', name='blog_detail'),
	url(r'^blog/(?P<id>\d{1,3})/edit/$', 'blog_edit', name='blog_edit'),
	url(r'^tag/(?P<name>\w{1,20})', 'tag_blogs', name='tag_blogs'),
)
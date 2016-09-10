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
	url(r'^datatable$', 'datatable'),

	url(r'^search/(?P<flag>\w{1,20})/$', 'search', name='search'),
	url(r'^home/$', 'blogs', name='home'),
	url(r'^blogs/$', 'blogs', name='blogs'),
	url(r'^blog/add/$', 'blog_add', name='blog_add'),
	url(r'^blog/(?P<id>\d{1,3})/detail/$', 'blog_detail', name='blog_detail'),
	url(r'^blog/(?P<id>\d{1,3})/edit/$', 'blog_edit', name='blog_edit'),
	url(r'^blog/(?P<id>\d{1,3})/delete/$', 'blog_del', name='blog_del'),

	url(r'^tags/$', 'tags', name='tags'),
	url(r'^tag/add$', 'tag_add', name='tag_add'),
	url(r'^tag/(?P<id>\d{1,3})/edit/$', 'tag_edit', name='tag_edit'),
	url(r'^tag/(?P<id>\d{1,3})/delete/$', 'tag_del', name='tag_del'),
	url(r'^tag/(?P<name>\w{1,20})/blogs/', 'tag_blogs', name='tag_blogs'),

	url(r'^categories/$', 'categories', name='categories'),
	url(r'^category/add$', 'category_add', name='category_add'),
	url(r'^category/(?P<id>\d{1,3})/modify/$', 'category_modify', name='category_modify'),
	url(r'^category/(?P<id>\d{1,3})/delelte$', 'category_del', name='category_del'),
	url(r'^category/(?P<catid>\d{1,3})/add/$', 'category_add_blog', name='category_add_blog'),
	url(r'^category/(?P<catid>\d{1,3})/edit/(?P<blogid>\d{1,3})/$', 'category_edit_blog', name='category_edit_blog'),
	url(r'^category/(?P<catid>\d{1,3})/delete/(?P<blogid>\d{1,3})/$', 'category_del_blog', name='category_del_blog'),
)
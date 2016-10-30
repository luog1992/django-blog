from django.contrib.auth.views import login, logout
from django.conf.urls import patterns, url, include
from django.views.generic import RedirectView
from django.contrib import admin
admin.autodiscover()

from article import views as articleviews


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^summernote/', include('django_summernote.urls')),
)

urlpatterns += patterns('article.views',
	url(r'^test/request/$', 'test_request'),
	url(r'^test/datatable$', 'test_datatable'),
	url(r'^test/celery$', 'test_celery'),

	url(r'^login/$', 'login', name='login'),
	url(r'^logout/$', 'logout', name='logout'),

	url(r'^search/(?P<flag>\w{1,20})/$', 'search', name='search'),

	url(r'^$', RedirectView.as_view(pattern_name='blogs', permanent=False), name='index'),
	url(r'^home/$', RedirectView.as_view(pattern_name='blogs', permanent=False), name='home'),
	url(r'^blogs/$', 'blogs', {'filter': 'blog', 'name': 'all'}, name='blogs'),
	url(r'^(?P<filter>\w{1,20})/(?P<name>\w{1,20})/blogs/', 'blogs', name='filter_blogs'),
	url(r'^blog/add/$', 'blog_add', name='blog_add'),
	url(r'^blog/(?P<id>\d{1,3})/detail/$', 'blog_detail', name='blog_detail'),
	url(r'^blog/(?P<id>\d{1,3})/delete/$', 'blog_del', name='blog_del'),
	url(r'^blog/(?P<id>\d{1,3})/modify/$',
		'request_splitter',
		{'GET': articleviews.blog_edit_get, 'POST': articleviews.blog_edit_post},
		name='blog_edit_splitter'
	),

	url(r'^tags/$', 'tags', name='tags'),
	url(r'^tag/add$', 'tag_add', name='tag_add'),
	url(r'^tag/(?P<id>\d{1,3})/delete/$', 'tag_del', name='tag_del'),
	url(r'^tag/(?P<id>\d{1,3})/modify/$',
		'request_splitter',
		{'GET': articleviews.tag_edit_get, 'POST': articleviews.tag_edit_post},
		name='tag_edit'
	),

	url(r'^categories/$', 'categories', name='categories'),
	url(r'^category/add$', 'category_add', name='category_add'),
	url(r'^category/(?P<id>\d{1,3})/delelte$', 'category_del', name='category_del'),
	url(r'^category/(?P<id>\d{1,3})/modify/$',
		'request_splitter',
		{'GET': articleviews.cat_modify_get, 'POST': articleviews.cat_modify_post},
		name='category_modify'
	),

	url(r'^category/(?P<catid>\d{1,3})/add/$', 'cat_add_blog', name='cat_add_blog'),
	url(r'^category/(?P<catid>\d{1,3})/delete/(?P<blogid>\d{1,3})/$', 'cat_del_blog', name='cat_del_blog'),
	url(r'^category/(?P<catid>\d{1,3})/edit/(?P<blogid>\d{1,3})/$',
		'request_splitter',
		{'GET': articleviews.cat_edit_blog_get, 'POST': articleviews.cat_edit_blog_post},
		name='cat_edit_blog'
	),
)

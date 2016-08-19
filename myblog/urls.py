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
	url(r'^$', RedirectView.as_view(url='/home/'), name='index'),
    url(r'^home/$', 'home', name='home'),
	url(r'^article/(?P<id>\d)/$', 'article', name='article'),
)
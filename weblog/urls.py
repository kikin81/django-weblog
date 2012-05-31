from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
import settings
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^css/(?P<path>.*)$', 'django.views.static.serve', 
        { 'document_root': settings.PROJECT_ROOT + '/css/' }),

    url(r'^search/$', 'weblog.search.views.search'),

    url(r'^comments', include('django.contrib.comments.urls')),

    url(r'^tags/', include('mingus.urls.tags')),

    url(r'^accounts/',  include('my_auth.urls')),

    url(r'', include('mingus.urls.entries')),
)

urlpatterns += staticfiles_urlpatterns()
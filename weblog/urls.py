from django.conf.urls import patterns, include, url
from django.contrib import admin
import settings
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tiny_mce/(?P<path>.*)$', 'django.views.static.serve', 
        { 'document_root': settings.PROJECT_ROOT + '../public/js/tiny_mce/' }),
    url(r'^weblog/tags/$', include('mingus.urls.tags')),
    url(r'^weblog/', include('mingus.urls.entries')),
)

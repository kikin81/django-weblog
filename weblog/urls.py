from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^comments/posted/$', 'mingus.views.comment_posted'),

    url(r'^comments/', include('django.contrib.comments.urls')),

    url(r'^search/$', 'mingus.views.search'),

    url(r'^tags/', include('mingus.urls.tags')),

    url(r'^add/tags/?$', 'mingus.views.newTag'),

    url(r'^accounts/',  include('my_auth.urls')),

    url(r'', include('mingus.urls.entries')),
)

urlpatterns += staticfiles_urlpatterns()

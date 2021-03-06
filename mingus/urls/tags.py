from django.conf.urls.defaults import *

from mingus.models import Tag

urlpatterns = patterns('',

    url(r'^$',
        'django.views.generic.list_detail.object_list',
        {'queryset': Tag.objects.all()},
        'mingus_tag_list'),

    url(r'^(?P<slug>[-\w]+)/$',
        'mingus.views.tag_detail',
        {},
        'mingus_tag_detail'),
)

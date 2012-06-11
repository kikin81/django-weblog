"""
URLS for blog_entries
"""
from django.conf.urls.defaults import *
from django.conf import settings

from mingus.models import Entry

PAGINATE_BY = getattr(settings, 'BLOG_ENTIRES_PAGINATE_BY', 15)

entry_info_dict = {
    'queryset': Entry.live.all(),
    'date_field': 'pub_date',
}

urlpatterns = patterns('django.views.generic.date_based',

    url(r'^(?P<year>\d{4})/$',
        'archive_year',
        entry_info_dict,
        'mingus_entry_archive_year'),

    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/$',
        'archive_month',
        entry_info_dict,
        'mingus_entry_archive_month'),

    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$',
        'archive_day',
        entry_info_dict,
        'mingus_entry_archive_day'),

    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        'object_detail',
        entry_info_dict,
        'mingus_entry_detail'),
)

urlpatterns += patterns('',
    url(r'^$',
        'mingus.views.entries_index',
        {'paginate_by': PAGINATE_BY},
        'mingus_entries_index'),
    url(r'^create/$',
        'mingus.views.create_entry',
        {},
        'mingus_create_entry'),
)

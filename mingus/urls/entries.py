from django.conf.urls.defaults import *

from mingus.models import Entry

entry_info_dict = {
    'queryset': Entry.live.all(),
    'date_field': 'pub_date',
}

urlpatterns = patterns('',
    url(r'', 'mingus.views.entries_index'),
)

urlpatterns += patterns('django.views.generic.date_based',
    
    (r'^(?P<year>\d{4})/$',
        'archive_year',
        entry_info_dict,
        'mingus_entry_archive_year'),
    
    (r'^(?P<year>\d{4})/(?P<month>\w{3})/$',
        'archive_month',
        entry_info_dict,
        'mingus_entry_archive_month'),
    
    (r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$',
        'archive_day',
        entry_info_dict,
        'mingus_entry_archive_day'),
    
    (r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        'object_detail',
        entry_info_dict,
        'mingus_entry_detail'),
)
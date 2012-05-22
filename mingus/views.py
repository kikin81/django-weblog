from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response
from mingus.models import Entry

def entries_index(request):
    entry_list = Entry.live.all()
    paginator = Paginator(entry_list, 3) # Show 3 entries per page

    page = request.GET.get('page')
    try:
        entries = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        entries = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        entries = paginator.page(paginator.num_pages)

    return render_to_response('mingus/entry_index.html', {"entries": entries})
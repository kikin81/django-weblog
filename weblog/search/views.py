from django.shortcuts import render_to_response
from mingus.models import Entry
from django.http import HttpResponseRedirect

def search(request):
    query = request.GET.get('q', '')
    keyword_results = []
    results = []
    if query:
        keyword_results = Entry.objects.filter(searchkeyword__keyword__in=query.split()).distinct()
        if keyword_results.count() == 1:
            return HttpResponseRedirect(keyword_results[0].get_absolute_url())
        resultTitle = Entry.objects.filter(title__icontains=query)
        resultBody = Entry.objects.filter(body__icontains=query)
    return render_to_response('search/search.html', {
        'query': query,
        'keyword_results': keyword_results,
        'resultTitle': resultTitle,
        'resultBody': resultBody,
    });
    
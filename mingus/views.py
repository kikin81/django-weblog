from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect, render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.utils import simplejson
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic.list_detail import object_list
from forms import EntryForm
from mingus.models import Entry, Tag


def entries_index(request, paginate_by):
    """
    Main listing:
      Displays live entries and paginates by the static variable paginate_by
    """
    entry_list = Entry.live.all()
    paginator = Paginator(entry_list, paginate_by) # Show 3 entries per page
    page = request.GET.get('page')
    try:
        entries = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        entries = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        entries = paginator.page(paginator.num_pages)

    if request.user.is_authenticated():
        # Do something for logged-in users.
        return render_to_response('mingus/entry_index.html',
                                  {"entries": entries},
                                  context_instance=RequestContext(request))
    else:
        # Do something for anonymous users.
        return render_to_response('mingus/entry_index.html', {"entries": entries})


@login_required
def create_entry(request):
    """
    Create entry:
      Model form which automatically fills in the author and uses slugify to 
      create a slug for the entry based on the tittle.
    """
    if request.method == 'POST':
        try:
            user = User.objects.get(username = request.user)
            new_entry = Entry(author=user)
            form = EntryForm(request.POST, instance=new_entry)
        except User.DoesNotExist:
            return HttpResponse("Invalid username")
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.slug = slugify(new_entry.title)
            new_entry.save()
            return HttpResponseRedirect("/")
    else:
        form = EntryForm()

    return render_to_response("mingus/create_entry.html",
                              {"form": form,},
                              context_instance=RequestContext(request))


def tag_detail(request, slug):
    """
    Tag detail:
      Displays live tags.
    """
    tag = get_object_or_404(Tag, slug=slug)
    return object_list(request, queryset=tag.live_entry_set(), extra_context={
        'tag': tag
    })

def tag_lookup(request):
    # Default return list
    results = []
    if request.method == "GET":
        if request.GET.has_key(u'q'):
            value = request.GET[u'q']
            # Ignore queries shorter than length 2
            if len(value) > 2:
               TI = Tag.objects.filter(name__startswith=value.lower())
               results = [ x.name for x in TI]
    return HttpResponse('\n'.join(results), mimetype='text/plain')


def search(request):
    query = request.GET.get('q', '')
    keyword_results = []
    results = []
    if query:
        keyword_results = FlatPage.objects.filter(searchkeyword__keyword__in=query.split()).distinct()
        if keyword_results.count() == 1:
            return HttpResponseRedirect(keyword_results[0].get_absolute_url())
        results = FlatPage.objects.filter(content__icontains=query)
    return render_to_response('mingus/search.html', {
        'query': query,
        'keyword_results': keyword_results,
        'results': results
    });
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect, render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.utils.html import escape
from forms import EntryForm, TagForm, forms
from mingus.models import Entry, Tag


def entries_index(request, paginate_by):
    """
    View of the latest entries published. This is similar to
    the :view:'django.views.generic.date_based.archive_index'
    generic view.
    **Template**
    ''mingus/entry_archive.html''
    **Context:**
    ''latest''
      A list of :model'mingus.Entry' objects.
    """
    entry_list = Entry.live.all()
    paginator = Paginator(entry_list, paginate_by)  # Show 3 entries per page
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


def comment_posted(request):
    """
    """
    return render_to_response('/')


@login_required
def create_entry(request):
    """
    Create entry:
      Model form which automatically fills in the author and uses slugify to
      create a slug for the entry based on the tittle.
    """
    if request.method == 'POST':
        try:
            user = User.objects.get(username=request.user)
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
                              {"form": form, },
                              context_instance=RequestContext(request))


def handlePopAdd(request, addForm, field):
    """
    View that handles the popup-add (new object) form.
    """
    if request.method == "POST":
        form = addForm(request.POST)
        if form.is_valid():
            try:
                newObject = form.save(commit=False)
                newObject.slug = slugify(newObject.title)
                newObject.save()
            except forms.ValidationError:
                newObject = None
            if newObject:
                return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % \
                    (escape(newObject._get_pk_val()), escape(newObject)))

    else:
        form = addForm()

    pageContext = {'form': form, 'field': field}
    return render_to_response("mingus/popup.html", pageContext, context_instance=RequestContext(request))


@login_required
def newTag(request):
    """
    View that handles a request for a new Tag.
    Instanciates a TagForm and calls handlePopAdd view.
    """
    return handlePopAdd(request, TagForm, 'tags')


def tag_detail(request, slug):
    """
    Tag detail:
      Displays live tags.
    """
    tag = get_object_or_404(Tag, slug=slug)
    return render_to_response('mingus/tag_detail.html',
                              {'object_list': tag.live_entry_set()})
    # return object_list(request, queryset=tag.live_entry_set(), extra_context={
    #     'tag': tag
    # })


def search(request):
    """
    Search View that handles blog entry search.
    Searches on title and body.
    """
    query = request.GET.get('q', '')
    keyword_results = []
    resultTitle = []
    resultBody = []
    if query:
        keyword_results = Entry.objects.filter(searchkeyword__keyword__in=query.split()).distinct()
        if keyword_results.count() == 1:
            return HttpResponseRedirect(keyword_results[0].get_absolute_url())
        resultTitle = Entry.objects.filter(title__icontains=query)
        resultBody = Entry.objects.filter(body__icontains=query)
    return render_to_response('mingus/search.html', {
        'query': query,
        'keyword_results': keyword_results,
        'resultTitle': resultTitle,
        'resultBody': resultBody,
    })

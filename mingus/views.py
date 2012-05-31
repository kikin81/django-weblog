from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.shortcuts import HttpResponseRedirect, render_to_response, get_object_or_404
from mingus.models import Entry, Tag
from django.views.generic.list_detail import object_list
from forms import EntryForm
from django.template.defaultfilters import slugify

def entries_index(request, paginate_by):
    """Main listing."""
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

def tag_detail(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    return object_list(request, queryset=tag.live_entry_set(), extra_context={
        'tag': tag
    })

@login_required
def create_entry(request):
    """Create new entry."""
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
from mingus.models import Entry, Tag
from django.forms import ModelForm
from datetime import date

class EntryForm(ModelForm):
    # how to handle tags
    # text entry with comma separated values?
    # click a + and a pop up comes with the tag form
    # if the request is successful, add it to the "list"
    class Meta:
        model = Entry
        exclude = ('author', 'slug',)

class TagForm(ModelForm):

    class Meta:
        model = Tag
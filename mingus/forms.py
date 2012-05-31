from mingus.models import Entry
from django.forms import ModelForm

from datetime import date

class EntryForm(ModelForm):
    class Meta:
        model = Entry
        exclude = ('author', 'slug')
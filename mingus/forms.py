from mingus.models import Entry, Tag
from mingus.widgets import MultipleSelectWithPop
from django.forms import ModelForm
from django import forms


class EntryForm(ModelForm):
    """
    Take advantage of Django's model form which builds a form based on the
    model. Exclude the author and slug from the form as these will be
    automatically calculated.

    """
    tags = forms.ModelMultipleChoiceField(Tag.objects, required=False, widget=MultipleSelectWithPop)

    class Meta:
        model = Entry
        exclude = ('author', 'slug',)


class TagForm(ModelForm):
    """
    Very simple Django Model form for the Tag model. Again, the slug field is
    excluded and calculated automatically in the view by applying slugify on
    the tag's title.

    """
    class Meta:
        model = Tag
        exclude = ('slug')

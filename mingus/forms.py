from django.contrib.auth.models import User
from mingus.models import Entry
from django import forms
import datetime

class EntryForm(forms.Form):
    #Title text
    #excerpt text
    #body text
    #pub date
    #author user
    #enable comments checkbox
    #featured checkbox
    #status live/draft/hidden
    #slug unique-generated from title
    #tags query-all-tags
    title = forms.CharField(max_length=250)
    excerpt = forms.CharField()
    body = forms.TextField()
    pub_date = forms.DateField(initial=datetime.date.today)
    enable_comments = forms.BooleanField()
    featured = forms.BooleanField()
    status = 


    def save(self):
        new_entry = Entry.objects.create_entry(title=title,
                                               excerpt=excerpt,
                                               body=body,
                                               pub_date=pub_date,
                                               author=author,
                                               enable_comments=enable_comments,
                                               featured=featured,
                                               status=status,
                                               slug=slug,
                                               tags=tags,)
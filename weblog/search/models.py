from django.db import models
from mingus.models import Entry

class SearchKeyword(models.Model):
    keyword = models.CharField(max_length=50)
    page = models.ForeignKey(Entry)
    
    def __unicode__(self):
        return self.keyword
from django.contrib import admin
from mingus.models import Tag, Entry

class EntryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}

admin.site.register(Entry, EntryAdmin)

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}

admin.site.register(Tag, TagAdmin)
from django.contrib import admin
from mingus.models import Tag, Entry


class EntryAdmin(admin.ModelAdmin):
    # Slugifies the title automatically and on the fly!
    prepopulated_fields = {'slug': ['title']}
    # Enables the horizontal filter for multi select
    filter_horizontal = ['tags']
admin.site.register(Entry, EntryAdmin)


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}
admin.site.register(Tag, TagAdmin)

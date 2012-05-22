from django.contrib import admin
from mingus.models import Tag

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}

admin.site.register(Tag, TagAdmin)
from django.contrib import admin
from models import Feed, Entry

class EntryInline(admin.TabularInline):
    model = Entry

class FeedAdmin(admin.ModelAdmin):
    list_display = ('title','url','subtitle','encoding','version')
    list_editable = ('url',)
    inlines = [EntryInline]
    
admin.site.register(Entry)
admin.site.register(Feed, FeedAdmin)
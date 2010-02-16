from django.contrib import admin
from models import Feed, Entry

class EntryInline(admin.TabularInline):
    model = Entry

class FeedAdmin(admin.ModelAdmin):
    list_display = ('title','url','subtitle','encoding','version')
    list_editable = ('url',)
    inlines = [EntryInline]
    
class EntryAdmin(admin.ModelAdmin):
    list_display = ('title','feed','link')
    
admin.site.register(Entry, EntryAdmin)
admin.site.register(Feed, FeedAdmin)
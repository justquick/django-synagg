from django.core.management.base import BaseCommand
from synagg.models import Feed, Entry
from feedparser import parse

class Command(BaseCommand):
    def handle(self, *urls, **options):
        for url in urls:
            feed,created = Feed.objects.get_or_create(url=url,data=parse(url))
            Entry.objects.filter(feed=feed).delete()
            for entry in feed.data.entries:
                Entry.objects.get_or_create(feed=feed,data=entry)
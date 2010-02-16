from django.core.management.base import BaseCommand
from synagg.models import Feed, Entry
import os

class Command(BaseCommand):
    def handle(self, *files_or_urls, **options):
        urls = []
        for f in files_or_urls:
            if f.startswith('http://') and not f in urls:
                urls.append(f)
            elif os.path.isfile(f):
                for l in open(f):
                    if not l.strip() in urls:
                        urls.append(l.strip())
        for url in urls:
            feed,created = Feed.objects.get_or_create(url=url)
            if not created:
                feed.save()

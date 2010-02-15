from django.db import models
from django.core.exceptions import ImproperlyConfigured
from django.db.models.signals import post_syncdb
from datetime import datetime

try:
    from picklefield import PickledObjectField
except ImportError:
    raise ImproperlyConfigured('You must install django-picklefield==0.1')
try:
    from feedparser import parse
except ImportError:
    raise ImproperlyConfigured('You must install feedparser==4.1')
    
    
class Feed(models.Model):
    url = models.URLField('RSS/Atom Feed URL')
    data = PickledObjectField()
    
    title = property(lambda self: self.data.feed.title)
    link = property(lambda self: self.data.feed.link)
    subtitle = property(lambda self: self.data.feed.subtitle)
    description = property(lambda self: self.data.channel.description)
    entries = property(lambda self: self.data.entries)
    version = property(lambda self: self.data.version)
    encoding = property(lambda self: self.data.encoding.lower())
    headers = property(lambda self: self.data.headers)
    
    def update(self, *a, **kw):
        data = self.data.copy()
        data.update(*a, **kw)
        self.data = data
        self.save()
        
    def save(self, *a, **kw):
        super(Feed, self).save(*a, **kw)
        for entry in self.entries:
            Entry.objects.get_or_create(feed=self,data=entry)

    def __unicode__(self):
        return self.title
    
class Entry(models.Model):
    feed = models.ForeignKey(Feed)
    data = PickledObjectField()

    title = property(lambda self: self.data.title)
    link = property(lambda self: self.data.link)
    updated_parsed = property(lambda self: datetime(*self.data.updated_parsed[:-2]))
    summary = property(lambda self: self.data.summary)
    
    def __unicode__(self):
        return self.title

def server_handler(created_models, **kw):
    if not Feed.objects.count():
        import os
        for url in open(os.path.join(os.path.dirname(__file__), 'feeds.txt')).readlines():
            url = url.strip()
            print 'Aggregating: %s' % url
            Feed.objects.create(url=url,data=parse(url))
post_syncdb.connect(server_handler)

from django.db import models
from django.core.exceptions import ImproperlyConfigured
from django.db.models.signals import post_syncdb
from datetime import datetime, timedelta

try:
    from feedparser import parse
    from tidylib import tidy_fragment
    from picklefield import PickledObjectField
except ImportError:
    raise ImproperlyConfigured('You must install pytidylib, django-picklefield==0.1 and feedparser==4.1')
    
class Feed(models.Model):
    url = models.URLField('RSS/Atom Feed URL',unique=True)
    data = PickledObjectField()
    last_updated = models.DateTimeField(blank=True,null=True)
    update_every = models.IntegerField(default=3600)
    
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
        if not self.last_updated or self.last_updated < datetime.now()+timedelta(seconds=self.update_every):
            print 'Aggregating: %s' % self.url
            data = parse(self.url)
            data.pop('bozo_exception',None)
            self.data = data
            self.last_updated = datetime.now()
            self.entry_set.all().delete()
            super(Feed, self).save(*a, **kw)
            for entry in data.entries:
                Entry.objects.get_or_create(feed=self,data=entry)
        return super(Feed, self).save(*a, **kw)
    
    def __unicode__(self):
        return self.title
    
class Entry(models.Model):
    feed = models.ForeignKey(Feed)
    data = PickledObjectField()

    title = property(lambda self: self.data.title)
    link = property(lambda self: self.data.link)
    updated_parsed = property(lambda self: datetime(*self.data.updated_parsed[:-2]))
    summary = property(lambda self: tidy_fragment(self.data.summary)[0])
    tease = property(lambda self: self.summary.split('. ')[0])
    
    def __unicode__(self):
        return self.title

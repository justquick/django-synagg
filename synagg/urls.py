from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail, object_list
from models import Entry,Feed

urlpatterns = patterns('synagg.views',
     (r'^(?P<object_id>\d+)/?$', object_detail, {'queryset':Feed.objects.all()}),
     (r'', object_list, {'queryset':Feed.objects.all()}),
)

from django.conf.urls import patterns, url
from edito313.content.views import ContentListView, ContentDetailView

urlpatterns = patterns('',
                       url(r'^(?P<uri>.*?[^/])$', ContentDetailView.as_view()),
                       url(r'^(?P<uri>.*)/$', ContentListView.as_view()),
                       url(r'^$', ContentListView.as_view()),
                       )

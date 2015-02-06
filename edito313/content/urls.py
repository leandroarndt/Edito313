from django.conf.urls import patterns, url
from edito313.content.views import ContentListView, ContentDetailView

urlpatterns = patterns('',
                       url(r'^(?P<pk>\d+)/$', ContentDetailView.as_view(),
                           name='content detail'),
                       url(r'^$', ContentListView.as_view()),
                       )

from django.conf.urls import patterns, include, url
from django.contrib import admin

# TODO: Load patterns from disk or create them if none is found 
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'edito313.views.home', name='home'),
    
    #discover.DownloadedPlugin.urls,

    url(r'^django/', include(admin.site.urls)),
    url(r'^', include('content.urls')),
    (r'^comments/', include('djangospam.cookie.urls')),
    #(r'^spam/', include('django.contrib.comments.urls')),
)
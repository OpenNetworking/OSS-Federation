from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'session_security/', include('session_security.urls')),
    url(r'', include('accounts.urls', namespace='accounts')),
)

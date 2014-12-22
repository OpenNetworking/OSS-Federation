from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r'^issuers/', views.issuers_api, name='issuers'),
    url(r'^colors/', views.colors_api, name='colors'),
)

from django.conf.urls import patterns, include, url
from . import views 

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'oss.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^polis/', views.polis_api, name='polis'),
    url(r'^colors', views.colors_api, name='colors'),

)

from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r'^login/$', views.account_login, name='account_login'),
    url(r'^logout/$', views.account_logout, name='account_logout'),
    url(r'^signup/$', views.account_signup, name='account_signup'),
    url(r'^$', views.home, name='home'),
    url(r'^profile/$', views.account_profile, name='account_profile'),
    url(r'^update/$', views.account_update, name='account_update'),
    url(r'^add_color/$', views.account_add_color,
        name='account_add_color'),
    url(r'^qqsend/$', views.qq_send, name='qq_send'),
)

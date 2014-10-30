from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'oss.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^create', views.issuer_create, name='issuer_create'),
    url(r'^delete', views.issuer_delete, name='issuer_delete'),
    url(r'^update', views.issuer_update, name='issuer_update'),
    url(r'^(?P<pk>\d+)/detail/$',
        views.IssuerDetailView.as_view(),
        name='issuer_detail'),

    url(r'^(?P<pk>\d+)/add_color/$',
        views.issuer_add_color, name='issuer_add_color'),
    url(r'^(?P<issuer_pk>\d+)/update_color/(?P<color_pk>\d+)/$',
        views.issuer_update_color, name='issuer_update_color'),
    url(r'^list', views.IssuerListView.as_view(), name='issuer_list'),
    url(r'^unconfirm_list', views.IssuerListView.as_view(), name='issuer_list'),

)

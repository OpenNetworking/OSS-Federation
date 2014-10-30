from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from .forms import AdminappAuthenticationForm
from . import views
from oss.apps.issuer.views import (IssuerListView,
                                   UnconfirmedIssuerListView)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'oss.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index, name='index'),
    url(r'^txs_list/', views.txs_list, name='txs_list'),
    url(r'^login/', login,
        dict(template_name="adminapp/login.html",
             authentication_form=AdminappAuthenticationForm),
        name='login'),
    url(r'^logout/', logout,
        dict(next_page='/adminapp/login'), name='logout'),
    url(r'^issuer_list/', views.IssuerListView.as_view(),
        name='issuer_list'),
    url(r'^new_issuer_list/',
        views.AdminUnconfirmedIssuerListView.as_view(),
        name='new_issuer_list'),
    url(r'^issuer_create/', views.admin_issuer_create,
        name='issuer_create'),
    url(r'^issuer_detail/(?P<pk>\d+)/',
        views.AdminIssuerDetailView.as_view(),
        name='issuer_detail'),
    url(r'^(?P<pk>\d+)/add_color/$', views.admin_issuer_add_color,
        name='issuer_add_color'),
    url(r'^(?P<issuer_pk>\d+)/update_color/(?P<color_pk>\d+)/$',
        views.admin_issuer_update_color, name='issuer_update_color'),

)

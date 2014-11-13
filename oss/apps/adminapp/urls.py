from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout

from .forms import AdminappAuthenticationForm
from . import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'oss.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index, name='index'),
    url(r'^txs_list/$', views.txs_list, name='txs_list'),
    url(r'^login/', login,
        dict(template_name="adminapp/login.html",
             authentication_form=AdminappAuthenticationForm),
        name='login'),
    url(r'^logout/$', logout,
        dict(next_page='/adminapp/login'), name='logout'),
    url(r'^issuer_list/', views.AdminIssuerListView.as_view(),
        name='issuer_list'),
    url(r'^unconfirmed_issuer_list/',
        views.AdminUnconfirmedIssuerListView.as_view(),
        name='unconfirmed_issuer_list'),
    url(r'^issuer_create/', views.admin_issuer_create,
        name='issuer_create'),
    url(r'^issuer_detail/(?P<pk>\d+)/$',
        views.AdminIssuerDetailView.as_view(),
        name='issuer_detail'),
    url(r'^issuer_delete/(?P<pk>\d+)/$',
        views.admin_issuer_delete,
        name='issuer_delete'),
    url(r'^(?P<pk>\d+)/add_color/$', views.admin_issuer_add_color,
        name='issuer_add_color'),
    url(r'^color_list/$', views.AdminColorListView.as_view(),
        name='color_list'),
    url(r'^unconfirmed_color_list/$',
        views.AdminUnconfirmedColorListView.as_view(),
        name='unconfirmed_color_list'),

)

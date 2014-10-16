from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from .forms import AdminappAuthenticationForm
from . import views 

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'oss.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index, name='index'),
    url(r'^login/', login, dict(template_name="adminapp/login.html",
                                authentication_form=AdminappAuthenticationForm)
                                ,name='login'),
    url(r'^logout/', logout, dict(next_page='/adminapp/login'), name='logout'),
    url(r'^polis_list/', views.polis_list, name='polis_list'),
    url(r'^new_polis_list/(?P<pk>\d+)/confirm/$', views.polis_owner_confirm, name='polis_owner_confirm'),
    url(r'^new_polis_list/create/$', views.polis_owner_create, name='polis_owner_create'),
    url(r'^new_polis_list/', views.new_polis_list, name='new_polis_list'),

)

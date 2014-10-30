from django.conf.urls import patterns, include, url
from . import views 
from django.contrib.auth.views import login, logout
from .forms import HomeAuthenticationForm

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'oss.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^index/$', views.index, name='index'),
    url(r'^login/$', login, 
        kwargs=dict(template_name='home/login.html',
                    authentication_form=HomeAuthenticationForm),
                    name='login'),
    url(r'^logout/$', logout, 
        kwargs=dict(next_page='/home/index/'),
        name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
)

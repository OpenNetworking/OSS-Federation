from django.conf.urls import patterns, include, url
from . import views 
from django.contrib.auth.views import login

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'oss.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^index/$', views.index, name='index'),
    url(r'signin/$', login, kwargs=dict(template_name='home/login.html'), name='signin'),
    url(r'logout/$', views.signout, name='signout'),
)

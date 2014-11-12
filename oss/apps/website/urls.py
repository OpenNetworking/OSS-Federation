from django.conf.urls import patterns, include, url
from . import views 
from django.contrib.auth.views import login, logout
from .forms import HomeAuthenticationForm

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'oss.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^login/$', login,
        kwargs=dict(template_name='website/login.html',
                    authentication_form=HomeAuthenticationForm),
                    name='login'),
    url(r'^logout/$', logout,
        kwargs=dict(next_page='/website/login/'),
        name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^waiting/$', views.waiting, name='waiting'),
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^update/$', views.WebsiteIssuerUpdateView.as_view(),
        name='issuer_update'),
    url(r'^add_color', views.add_color, name='add_color'),
    url(r'^(?P<pk>\d+)/color_detail/$',
        views.WebsiteColorDetailView.as_view(), name='color_detail'),

)

from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'oss.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'session_security/', include('session_security.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^chart/', include('chart.urls', namespace='chart')),
    url(r'^adminapp/', include('adminapp.urls', namespace='adminapp')),
    url(r'^issuer/', include('baseissuer.urls', namespace='baseissuer')),
)

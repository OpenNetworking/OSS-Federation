from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns

urlpatterns = patterns('',
    url(r'session_security/', include('session_security.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += i18n_patterns('',
    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^chart/', include('chart.urls', namespace='chart')),
    url(r'adminapp/', include('adminapp.urls', namespace='adminapp')),
    url(r'^issuer/', include('baseissuer.urls', namespace='baseissuer')),
)

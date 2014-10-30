from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'oss.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^api/', include('oss.apps.api.urls')),
    url(r'adminapp/', include('oss.apps.adminapp.urls', namespace='adminapp')),
    url(r'website/', include('oss.apps.website.urls', namespace='website')),
    url(r'^issuer/', include('oss.apps.issuer.urls', namespace='issuer')),
)

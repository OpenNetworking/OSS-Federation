from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
    url(r'^daily-tx-chart/$', views.daily_tx_chart, name='daily_tx_chart'),
    url(r'^monthly-tx-chart/$', views.monthly_tx_chart, name='monthly_tx_chart'),
    url(r'^yearly-tx-chart/$', views.yearly_tx_chart, name='yearly_tx_chart'),
    url(r'^fake/$', views.fakedata, name='fakedata'),
    url(r'^fakemonth/$', views.fakemonth, name='fakemonth'),
    url(r'^fakeyear/$', views.fakeyear, name='fakeyear'),
)

from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
    url(r'^daily-tx-chart/$', views.daily_tx_chart, name='daily_tx_chart'),
    url(r'^monthly-tx-chart/$', views.monthly_tx_chart, name='monthly_tx_chart'),
    url(r'^yearly-tx-chart/$', views.yearly_tx_chart, name='yearly_tx_chart'),
    url(r'^transaction-chart/$', views.transaction_chart,
        name="transaction_chart"),
    url(r'^network-status-chart/$', views.network_status_chart,
        name='network_status_chart'),
    url(r'^blockchain-status/$', views.blockchain_status,
        name='blockchain_status'),
    url(r'day/$', views.day, name="day"),
    url(r'^fake/$', views.fakedata, name='fakedata'),
    url(r'^fakemonth/$', views.fakemonth, name='fakemonth'),
    url(r'^fakeyear/$', views.fakeyear, name='fakeyear'),
    url(r'^qqq/$', views.qqq, name='qqq'),
    url(r'^eee/$', views.eee, name='eee'),
    url(r'api/aeinfo/', views.api_aeinfo, name="api_aeinfo"),
)

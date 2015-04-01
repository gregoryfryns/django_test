from django.conf.urls import patterns, url
from welcomepage import views

urlpatterns = patterns('',
    url(r'^$', views.welcomepage, name='home'),
)


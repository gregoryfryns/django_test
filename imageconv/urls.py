from django.conf.urls import patterns, url
from imageconv import views

urlpatterns = patterns('',
    url(r'^$', views.imageconv, name='upload'),
)

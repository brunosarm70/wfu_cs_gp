from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^home/', views.home),
    url(r'^games/', views.games),
]

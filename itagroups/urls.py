from django.conf.urls import include, url
from django.contrib import admin

from groups import views

urlpatterns = [
    # Examples:
    url(r'^$', views.home_page, name='home'),
    url(r'^groups/(.+)/$', views.view_group, name='view_group')
]

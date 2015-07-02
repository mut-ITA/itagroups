from django.conf.urls import include, url
from django.contrib import admin

from groups import views

urlpatterns = [
    # Examples:
    url(r'^$', views.home_page, name='home'),
    url(r'^groups/(.+)/$', views.view_group, name='view_group'),
    url(r'^login$', views.verify_login, name='verify_login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^signup/$', views.signup, name='sign_up'),
    url(r'^users/(.+)/$', views.view_user, name='view_user'),
    url(r'^users/me$', views.self_user, name='self_user'),
    url(r'^groups/(.+)/leave$', views.leave_group, name='leave_group')
]

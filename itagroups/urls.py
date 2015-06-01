from django.conf.urls import include, url
from django.contrib import admin

from groups import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'itagroups.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home_page, name='home')
]

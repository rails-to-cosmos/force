from django.conf.urls import url

import views


urlpatterns = [
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
    url(r'^current_user/$', views.current_user),
]

from django.conf.urls import url

import views


urlpatterns = [
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
    # url(r'^users/$', UserViewSet.as_view({'get': 'list'})),
    # url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    # TODO maybe make rest_framework auth
    # url(r'^', include('rest_framework.urls',
    #                   namespace='rest_framework')),
]

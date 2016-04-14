from django.conf.urls import include, url
from django.contrib import admin

from views import index

from rest_framework import routers

from authorization.viewsets import UserViewSet

from menu.viewsets import (MenuViewSet,
                           OrderViewSet)


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'menus', MenuViewSet)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index),
    url(r'^menu/', include('menu.urls')),
    url(r'^auth/', include('authorization.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls')),
]

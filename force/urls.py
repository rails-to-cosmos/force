from django.conf.urls import include, url
from django.contrib import admin

from views import index

from rest_framework import routers

from authorization.viewsets import UserViewSet

from menu.viewsets import (MenuViewSet,
                           OrderViewSet,
                           ProductViewSet)


router = routers.DefaultRouter()
viewsets = ((r'users', UserViewSet),
            (r'orders', OrderViewSet),
            (r'menus', MenuViewSet),
            (r'products', ProductViewSet))
for viewset in viewsets:
    router.register(*viewset)


urlpatterns = [
    url(r'^$', index),
    url(r'^admin/', admin.site.urls),
    url(r'^menu/', include('menu.urls')),
    url(r'^auth/', include('authorization.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls')),
]

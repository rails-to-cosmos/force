from __future__ import unicode_literals

from django.conf.urls import include, url
from django.contrib import admin

from rest_framework import routers

from authorization.viewsets import UserViewSet

from restaurant.viewsets.menu import MenuViewSet
from restaurant.viewsets.category import CategoryViewSet
from restaurant.viewsets.product import ProductViewSet
from restaurant.viewsets.order import OrderViewSet

router = routers.DefaultRouter()
viewsets = ((r'users', UserViewSet),
            (r'orders', OrderViewSet),
            (r'menus', MenuViewSet),
            (r'products', ProductViewSet),
            (r'categories', CategoryViewSet))
for viewset in viewsets:
    router.register(*viewset)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^rest/', include(router.urls)),
    url(r'^rest/', include('restaurant.urls')),
    # url(r'^auth/', include('authorization.urls')),
    url(r'^accounts/', include('rest_framework.urls')),
    url(r'^accounts/', include('djoser.urls')),
    url(r'^files/', include('db_file_storage.urls')),
    # url(r'^tokens/', include('djoser.urls.authtoken')),
]

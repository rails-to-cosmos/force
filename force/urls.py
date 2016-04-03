"""
force URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

from views import index

from rest_framework import routers

from authorization.viewsets import UserViewSet
from menu.viewsets import (MenuViewSet,
                           ProductViewSet,
                           CategoryViewSet,
                           OrderViewSet)


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'menu', MenuViewSet)
router.register(r'product', ProductViewSet)
router.register(r'category', CategoryViewSet)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index),
    url(r'^menu/', include('menu.urls')),
    url(r'^auth/', include('authorization.urls')),
    url(r'^api/', include(router.urls)),
]

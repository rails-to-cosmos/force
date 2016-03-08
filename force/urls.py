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
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib import admin

import rest_framework
from rest_framework import routers, serializers, viewsets
from rest_framework.authtoken import views


from authorization.viewsets import UserViewSet
from menu.viewsets import MenuViewSet, ProductViewSet, CategoryViewSet


router = routers.DefaultRouter()

router.register(r'users', UserViewSet)

router.register(r'menu', MenuViewSet)
router.register(r'product', ProductViewSet)
router.register(r'category', CategoryViewSet)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^menu/', include('menu.urls')),
    url(r'^authorization/', include('authorization.urls')),
    url(r'^api/', include(router.urls)),
    # url(r'^api/auth/', include('rest_framework.urls')),
    url(r'^api/auth/', views.obtain_auth_token),
]

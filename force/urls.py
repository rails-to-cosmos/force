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
from rest_framework import routers, serializers, viewsets
import views


# ViewSets define the view behavior.
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)


# api = Api(api_name='v1')
# api.register(ProductResource())
# api.register(MenuResource())

urlpatterns = [url(r'^admin/', admin.site.urls),
               # url(r'^', views.index),
               url(r'^$', TemplateView.as_view(template_name='index.html')),
               url(r'^menu/', include('menu.urls')),
               url(r'^authorization/', include('authorization.urls'))]
               # url(r'^api/', include(api.urls)),
               # url(r'^api/', include(router.urls))]

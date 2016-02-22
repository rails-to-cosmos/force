from django.conf.urls import include, url
from rest_framework import routers
from viewsets import UserViewSet
import views


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]

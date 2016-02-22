from rest_framework import routers
from django.conf.urls import url, include
from viewsets import MenuViewSet, ProductViewSet, CategoryViewSet
import views


router = routers.DefaultRouter()
router.register(r'list', MenuViewSet)
router.register(r'product', ProductViewSet)
router.register(r'category', CategoryViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    # url(r'^$', views.view_menu, name='menuview'),
    url(r'^load/', views.load_menu, name='menuload'),
]

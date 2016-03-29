from django.utils import timezone
from models import Menu, Product, Category, Order
from serializers import MenuSerializer, ProductSerializer, CategorySerializer, OrderSerializer
from rest_framework import viewsets


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.filter(date__gte=timezone.now())
    serializer_class = MenuSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

# -*- coding: utf-8 -*-

from django.utils import timezone

from models import Menu, Product, Category, Order
from serializers import MenuSerializer
from serializers import ProductSerializer
from serializers import CategorySerializer
from serializers import OrderSerializer

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from rest_framework.serializers import ValidationError
from rest_framework.decorators import list_route


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
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = request.user.orders.all()
        serializer = OrderSerializer(
            queryset,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    def perform_create(self, serializer):
        menu = serializer.validated_data.get('menu')
        product = serializer.validated_data.get('product')

        try:
            menu.products.get(id=product.id)
        except Product.DoesNotExist:
            raise ValidationError(u'Не пытайся меня наебать!')

        serializer.save(user=self.request.user,
                        date=timezone.now())

    @list_route(url_path='all', permission_classes=[IsAdminUser])
    def all(self, request):
        queryset = Order.objects.all()
        serializer = OrderSerializer(
            queryset,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

from models import Menu, Product, Category, Order
from rest_framework import serializers
from menu.permissions import IsOwnerOrAdmin


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ('category', 'weight', 'compound', 'cost', 'name')


class MenuSerializer(serializers.HyperlinkedModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = ('date', 'products')


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('name', )


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ('menu', 'product', 'user', 'count')

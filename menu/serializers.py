from models import Menu, Product, Category, Order
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', )


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('category', 'category_name',
                  'id', 'weight', 'compound', 'cost', 'name')


class MenuSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    weekday = serializers.SerializerMethodField('current_weekday')

    class Meta:
        model = Menu
        fields = ('id', 'date', 'products', 'weekday')

    def current_weekday(self, obj):
        return obj.date.weekday()


class OrderSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Order
        fields = ('menu', 'product', 'count', 'date')

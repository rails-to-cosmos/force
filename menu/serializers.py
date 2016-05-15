from models import Menu, Product, Category, Order
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', )


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('category_name',
                  'id', 'weight', 'compound', 'cost', 'name')


class MenuSerializer(serializers.ModelSerializer):
    weekday = serializers.SerializerMethodField('current_weekday')

    class Meta:
        model = Menu
        fields = ('id', 'date', 'weekday')

    def current_weekday(self, obj):
        return obj.date.weekday()


class OrderSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Order
        fields = ('menu', 'product', 'count', 'date')

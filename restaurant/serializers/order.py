from rest_framework import serializers
from ..models import Order


class OrderSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Order
        fields = ('menu', 'product', 'count', 'date')

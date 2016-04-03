from django.contrib.auth.models import User
from rest_framework import serializers

# from menu.models import Order


class UserSerializer(serializers.ModelSerializer):
    # orders = serializers.PrimaryKeyRelatedField(many=True,
    #                                             queryset=Order.objects.all())

    class Meta:
        model = User
        fields = ('url', 'username', 'first_name', 'last_name', 'email', 'is_staff')

from rest_framework import serializers
from ..models import Menu


class MenuSerializer(serializers.ModelSerializer):
    weekday = serializers.SerializerMethodField('current_weekday')

    class Meta:
        model = Menu
        fields = ('id', 'date', 'weekday')

    def current_weekday(self, obj):
        return obj.date.weekday()

from django.utils import timezone

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAdminUser
from rest_framework.serializers import ValidationError
from rest_framework.decorators import list_route

from ..exceptions import HACKER_ATTACK_MESSAGE
from ..models import Product, Order
from ..serializers.order import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, )

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
            raise ValidationError(HACKER_ATTACK_MESSAGE)

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

from django.utils import timezone

from rest_framework import viewsets, mixins
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response
from rest_framework.decorators import detail_route

from ..serializers.menu import MenuSerializer
from ..serializers.product import ProductSerializer
from ..models import Menu


class MenuViewSet(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = Menu.objects.filter(date__gt=timezone.now()).order_by('date')
    serializer_class = MenuSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly, )

    @detail_route(methods=['get'])
    def products(self, request, pk=None, format=None):
        queryset = self.get_object().products
        serializer = ProductSerializer(
            queryset,
            many=True,
            context={
                'request': request
            }
        )
        return Response(serializer.data)

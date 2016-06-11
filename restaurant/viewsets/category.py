from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from ..utils import (user_wants_actual_menu,
                     get_actual_menu,
                     extend_response)
from ..models import Category, Product
from ..serializers.category import CategorySerializer
from ..serializers.menu import MenuSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly, )

    def list(self, request):
        menu = None

        if user_wants_actual_menu(request):
            menu = get_actual_menu()
            actual_category_ids = Product.objects.filter(menu=menu).\
                values('category').distinct()
            categories = Category.objects.filter(pk__in=actual_category_ids)
            categories_serialized = self.serializer_class(
                categories,
                many=True,
                context={
                    'request': request
                }
            ).data
            response = categories_serialized
        else:
            response = CategorySerializer(
                Category.objects.all(),
                many=True,
                context={
                    'request': request
                }
            ).data

        response_extended = False

        if menu:
            menu_serialized = MenuSerializer(menu).data
            response, response_extended = extend_response(
                response,
                'menu',
                menu_serialized,
                'categories',
                response_extended
            )

        return Response(response)

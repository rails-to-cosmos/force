from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from ..utils import user_wants_actual_menu, get_actual_menu
from ..models import Category, Product
from ..serializers.category import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly, )

    def list(self, request):
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
            return Response(categories_serialized)
        else:
            return Response(CategorySerializer(
                Category.objects.all(),
                many=True,
                context={
                    'request': request
                }
            ).data)

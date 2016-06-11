from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response

from ..serializers.menu import MenuSerializer
from ..serializers.product import ProductSerializer
from ..utils import user_wants_actual_menu, get_actual_menu
from ..models import Category, Product


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly, )

    def list(self, request):
        menu = None
        if user_wants_actual_menu(request):
            menu = get_actual_menu()
            queryset = Product.objects.filter(menu=menu)
        else:
            queryset = Product.objects.all()

        serializer = ProductSerializer(
            queryset,
            many=True,
            context={
                'request': request
            }
        )
        products = serializer.data

        group = request.GET.get('group', '')
        if group == 'category':
            categories = Category.objects.order_by('order').all()
            response = {}
            category_cache = {}
            for product in products:
                category_id = product.get('category', '')
                if category_id not in category_cache:
                    for category in categories:
                        if category.id == category_id:
                            category_cache[category_id] = category.name
                            break

                category_name = category_cache.get(category_id)
                if category_name not in response:
                    response[category_name] = []
                response[category_name].append(product)
        else:
            response = products

        if menu:
            menu_serialized = MenuSerializer(menu).data
            response = {
                'products': response
            }
            response['menu'] = menu_serialized

        return Response(response)

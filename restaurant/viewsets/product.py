from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response

from ..serializers.menu import MenuSerializer
from ..serializers.category import CategorySerializer
from ..serializers.product import ProductSerializer

from ..utils import (user_wants_actual_menu,
                     user_filter_by_category,
                     get_actual_menu,
                     extend_response)
from ..models import Category, Product


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly, )

    def list(self, request):
        menu = None
        category = None

        if user_filter_by_category(request):
            category_id = int(request.GET.get('category'))
            category = Category.objects.filter(id=category_id).first()

        if user_wants_actual_menu(request):
            menu = get_actual_menu()
            if category:
                queryset = Product.objects.filter(menu=menu,
                                                  category=category)
            else:
                queryset = Product.objects.filter(menu=menu)
        else:
            if category:
                queryset = Product.objects.filter(category=category)
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

        response_extended = False

        if menu:
            menu_serialized = MenuSerializer(menu).data
            response, response_extended = extend_response(
                response,
                'menu',
                menu_serialized,
                'products',
                response_extended
            )

        if category:
            category_serialized = CategorySerializer(category).data
            response, response_extended = extend_response(
                response,
                'category',
                category_serialized,
                'products',
                response_extended
            )

        return Response(response)

from django.contrib.auth.models import User
from tastypie.authentication import Authentication
from tastypie.authentication import BasicAuthentication
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource

from menu.models import Product


class ProductResource(ModelResource):
    class Meta:
        queryset = Product.objects.all()
        resource_name = 'product'
        allowed_methods = ['post', 'get', 'put', 'delete']
        authentication = Authentication()
        authorization = DjangoAuthorization()
        always_return_data = True

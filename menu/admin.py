from django.contrib import admin

from models import (Menu, Category, Product, Document, Order)

modules = (Menu, Category, Product, Document, Order)

[admin.site.register(module) for module in modules]

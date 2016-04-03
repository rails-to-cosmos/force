from django.contrib import admin

from models import (Menu, Category, Product, Order)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    ordering = ['order']


class ProductAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'name', 'compound',
                    'weight', 'description', 'tags',
                    'added', 'cost')
    list_filter = ('category',)
    search_fields = ('name', 'description', 'compound')


class MenuAdmin(admin.ModelAdmin):
    list_display = ('date_fmt',)


modules = ((Menu, MenuAdmin),
           (Category, CategoryAdmin),
           (Product, ProductAdmin),
           (Order,))

for module in modules:
    admin.site.register(*module)

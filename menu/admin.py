from django.contrib import admin

from models import (Menu, Category, Product, Order)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'name', 'added_fmt', 'cost')
    list_filter = ('category',)


class MenuAdmin(admin.ModelAdmin):
    list_display = ('date_fmt',)


modules = ((Menu, MenuAdmin),
           (Category, CategoryAdmin),
           (Product, ProductAdmin),
           (Order,))
[admin.site.register(*module) for module in modules]

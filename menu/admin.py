from django.contrib import admin

from models import (Menu, Category, Product, Document, Order, XLStructure)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'name', 'cost')


class MenuAdmin(admin.ModelAdmin):
    list_display = ('date_fmt',)


class XLStructureAdmin(admin.ModelAdmin):
    list_display = ('menu', 'product', 'position')


modules = [(Menu, MenuAdmin),
           (Category, CategoryAdmin),
           (Product, ProductAdmin),
           (Document, ),
           (Order,),
           (XLStructure, XLStructureAdmin)]

[admin.site.register(*module) for module in modules]

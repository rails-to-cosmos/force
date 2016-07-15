from django.contrib import admin

from models import Menu, Category, Product, Attachment, Order


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    ordering = ['order']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'name', 'compound',
                    'weight', 'description', 'tags',
                    'added', 'cost')
    list_filter = ('category',)
    search_fields = ('name', 'description', 'compound')


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('date_fmt',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'count', 'menu', 'user', 'date')


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'upload_date', 'menufile')

# -*- coding: utf-8 -*-

from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from models import Menu, Category, Product, XLStructure

from classes.manager import MenuManager
from classes.downloader import download_menu_files


def view_menu(request):
    menu = Menu.objects.filter(date__gte=timezone.now()).order_by('date')[0]
    products = menu.products.all()

    categories_and_products = {}
    for product in products:
        try:
            categories_and_products[product.category.name][:0] = [{
                u'name': product.name,
                u'description': product.compound,
                u'cost': product.cost,
            }]
        except KeyError:
            categories_and_products[product.category.name] = [{
                u'name': product.name,
                u'description': product.compound,
                u'cost': product.cost,
            }]

    response = {
        u'products': []
    }

    for category, products in categories_and_products.iteritems():
        response[u'products'].append([category, products])

    return JsonResponse(response)

@login_required
def load_menu(request):
    def load_menu_from_file(menu_file):
        manager = MenuManager()
        manager.add_menus_from_file(menu_file)
        menus = manager.menus
        for menu in menus:
            menu.obj, created = Menu.objects.get_or_create(date=menu.date)
            for product in menu.products:
                category_obj, created = Category.objects.get_or_create(
                    name=product.category)
                product.obj, created = Product.objects.get_or_create(
                    cost=product.cost,
                    name=product.name,
                    defaults=dict(
                        category=category_obj,
                        weight=product.weight,
                        compound=product.compound,
                        added=menu.date
                    ))
                xls, created = XLStructure.objects.get_or_create(
                    menu=menu.obj,
                    product=product.obj,
                    position=product.position)
                menu.obj.products = [product.obj for product in menu.products]
                menu.obj.save()

    def fetch_menu():
        menu_files = download_menu_files()
        for menu_file in menu_files:
            load_menu_from_file(menu_file)

        # TODO return not only boolean
        return True

    if fetch_menu():
        response = JsonResponse({
            'success': u'Menu successfully loaded'
        })
        response.status_code = 200
    else:
        response = JsonResponse({
            'error': u'Unable to load menu'
        })
        response.status_code = 503

    return response

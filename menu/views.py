# -*- coding: utf-8 -*-

from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from models import Menu, Category, Product, XLStructure

from classes.manager import MenuManager
from classes.downloader import download_menu_files


def view_menu(request):
    # if now > 15:00, date__gte now
    # if now < 15:00, date_gte tomorrow
    menu = Menu.objects.filter(date__gte=timezone.now()).order_by('date')[0]
    categories = Category.objects.all().order_by('id').values('id', 'name')
    products = menu.products.all()

    products_grouped = {}
    for product in products:
        try:
            # prepend
            products_grouped[product.category.id][:0] = [{
                u'id': product.id,
                u'name': product.name,
                u'description': product.compound,
                u'cost': product.cost,
            }]
        except KeyError:
            products_grouped[product.category.id] = [{
                u'id': product.id,
                u'name': product.name,
                u'description': product.compound,
                u'cost': product.cost,
            }]

    response = {
        u'menu': {
            u'date': '',
            u'weekday': '',
        },
        u'products': []
    }

    for category in categories:
        response['products'].append((category.get('id'),
                                  category.get('name'),
                                  products_grouped.get(category.get('id'))))

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

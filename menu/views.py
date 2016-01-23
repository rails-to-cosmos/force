import os

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from models import Menu, Category, Product, XLStructure
from lib.menumanager import MenuManager


@login_required
def load_menu(request):
    load_menu_from_file(os.path.dirname(os.path.realpath(__file__)) + '/../lib/menu.xls')
    return HttpResponse('OK')


def load_menu_from_file(menu_file):
    manager = MenuManager()
    manager.add_menus_from_file(menu_file)
    sheets = manager.menus
    for sheet in sheets:
        products = sheet.products
        menu, created = Menu.objects.get_or_create(date=sheet.date)
        [XLStructure.objects.get_or_create(
            menu=menu,
            product=Product.objects.get_or_create(
                cost=x.cost,
                name=x.name,
                defaults=dict(
                    category=Category.objects.get_or_create(name=x.category)[0],
                    weight=x.weight,
                    compound=x.compound
                ))[0],
            position=x.position)
         for x in products]


def view_menu(request):
    return HttpResponse('Menu view page')

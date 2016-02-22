import os
import urllib
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from models import Menu, Category, Product, XLStructure
from classes.manager import MenuManager
from w2p.classes.processor import WebPageProcessor
from w2p.classes.actions.action import Action


@login_required
def load_menu(request):
    if fetch_menu():
        result = HttpResponse(u'Menu successfully loaded')
    else:
        result = HttpResponse(u'Unable to load menu')
    return result


def fetch_menu():
    menu_files = download_menu_files()
    for menu_file in menu_files:
        load_menu_from_file(menu_file)
    return True


def download_menu_files():
    menu_files = list()
    site_url = "http://hleb-sol.biz"
    wpp = WebPageProcessor()
    wpp.add_action(
        _type=Action.AT_FAST_DOWNLOAD,
        _name="webpage",
        _subject=site_url
    )
    wpp.add_action(
        _type=Action.AT_PARSE_BY_SELECTOR,
        _name="link",
        _target="webpage",
        _subject=".menuItemBig td a[href]",
        _visible=True
    )
    wpp.run()
    links = wpp.get_result()
    for lind, link in enumerate(links):
        rel_url = link.get('link')
        abs_url = site_url + rel_url
        upload_dir = 'static/uploads/'  # TODO move to settings
        os.path.exists(upload_dir) or os.makedirs(upload_dir)
        filename = u'{dt}-{di}.xls'.format(dt=unicode(timezone.now()),
                                           di=lind)
        urllib.urlretrieve(abs_url, upload_dir+filename)
        menu_files.append(upload_dir+filename)
    return menu_files


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
                    compound=product.compound
                ))
            xls, created = XLStructure.objects.get_or_create(
                menu=menu.obj,
                product=product.obj,
                position=product.position)
        menu.obj.products = [product.obj for product in menu.products]
        menu.obj.save()

def view_menu(request):
    return render(request,
                  'menu/view.html',
                  {'param': '123'})

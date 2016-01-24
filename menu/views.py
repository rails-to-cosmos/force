import urllib
from datetime import datetime

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from models import Menu, Category, Product, XLStructure
from lib.menumanager import MenuManager
from w2p.classes.processor import WebPageProcessor
from w2p.classes.actions.action import Action


@login_required
def load_menu(request):
    menu_files = download_menu_files()
    for menu_file in menu_files:
        load_menu_from_file(menu_file)
    return HttpResponse('Menus have been successfully loaded')


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
        fpath = 'staticfiles/uploads/{dt}-{di}.xls'.format(dt=str(datetime.now()),
                                                           di=lind)
        urllib.urlretrieve(abs_url, fpath)
        menu_files.append(fpath)
    return menu_files


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

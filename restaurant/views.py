from __future__ import unicode_literals
from builtins import range

from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.files import File

import mimetypes
import urllib
import os
import xlrd
import xlwt
from xlutils.copy import copy as xlcopy

from rest_framework import status

from models import (Menu,
                    Category,
                    Product,
                    Order,
                    XLStructure,
                    Attachment)

from classes.manager import MenuManager
from classes.downloader import download_menu_files

from cyrdp.dateparser import DateParser


def load_menu_from_file(menu_file, attachment):
    manager = MenuManager()
    manager.add_menus_from_file(menu_file)

    menus = manager.menus
    for date, products_json in menus.iteritems():
        menu, menu_created = Menu.objects.get_or_create(date=date,
                                                        attachment=attachment)

        products = []
        for product_json in products_json:
            category, category_created = Category.objects.get_or_create(
                name=product_json.get('category', 'default_category'))

            product, product_created = Product.objects.get_or_create(
                hash=Product.calculate_hash(
                    product_json.get('name', ''),
                    product_json.get('compound', ''),
                    product_json.get('weight', '')
                ),
                defaults={
                    'cost': product_json.get('cost', ''),
                    'name': product_json.get('name', ''),
                    'category': category,
                    'weight': product_json.get('weight'),
                    'compound': product_json.get('compound'),
                    'added': date
                }
            )

            xls, xls_created = XLStructure.objects.get_or_create(
                menu=menu,
                product=product,
                position=product_json.get('row')
            )

            products.append(product)

        menu.products = products
        menu.save()


def fetch_menu():
    # get provider, provider->get_fresh_menus
    menu_files = download_menu_files()

    for menu_file in menu_files:
        with open(menu_file, 'r') as mf:
            fs = Attachment(path=File(mf))
            fs.save()
            load_menu_from_file(menu_file, fs)

    # TODO verbose output
    return True


@login_required
def load_menu(request):
    try:
        fetch_menu()
    except:
        response = JsonResponse({
            'error': 'Unable to load menu'
        })
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    else:
        response = JsonResponse({
            'success': 'Menu successfully loaded'
        })
        response.status_code = status.HTTP_200_OK

    # TODO verbose output
    return response


@login_required
def get_menu(request):
    menu = Menu.get_current_menu()
    contents = menu.attachment.path.read()

    tmp_filename = '/tmp/tmp.xls'
    tmp_xls = open(tmp_filename, 'w')
    tmp_xls.write(contents)
    tmp_xls.close()

    read_book = xlrd.open_workbook(tmp_filename, on_demand=True, formatting_info=True)
    write_book = xlcopy(read_book)

    dp = DateParser()
    menu_date = dp.parse(str(menu.date))
    for sheet_index in range(len(write_book._Workbook__worksheets)):
        write_sheet = write_book.get_sheet(sheet_index)
        sheet_date = dp.parse(write_sheet.name)
        if sheet_date == menu_date:
            break
    else:
        raise Exception('Sheet not found!')

    orders = Order.objects.filter(menu=menu)
    ppixs = XLStructure.objects.filter(product__in=orders.values_list('product'), menu=menu)

    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.bold = True
    font.height = 12*20
    font.name = 'Calibri'
    style.font = font
    borders = xlwt.Borders()
    borders.bottom = xlwt.Borders.THIN
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    borders.left = xlwt.Borders.THIN
    style.borders = borders
    total_cell_style = xlwt.XFStyle()
    total_cell_style.font = font
    total = 0
    total_row_pos = XLStructure.objects.filter(menu=menu).order_by('-position').first().position + 1

    for ppix in ppixs:
        count = sum(order.count for order in orders.filter(product=ppix.product))
        cost = ppix.product.cost * count
        write_sheet.write(ppix.row_in_xls, 4, count, style=style)
        write_sheet.write(ppix.row_in_xls, 5, cost, style=style)
        total += cost
    write_sheet.write(total_row_pos, 5, total, style=total_cell_style)
    write_book.save(tmp_filename)

    tmp_xls = open(tmp_filename)
    response = HttpResponse(tmp_xls.read(), content_type='application/vnd.ms-excel')
    tmp_xls.close()

    _type, encoding = mimetypes.guess_type(tmp_filename)
    if _type is None:
        _type = 'application/octet-stream'
    response['Content-Type'] = _type
    response['Content-Length'] = str(os.stat(tmp_filename).st_size)
    if encoding is not None:
        response['Content-Encoding'] = encoding

    # To inspect details for the below code, see http://greenbytes.de/tech/tc2231/
    if u'WebKit' in request.META['HTTP_USER_AGENT']:
        # Safari 3.0 and Chrome 2.0 accepts UTF-8 encoded string directly.
        filename_header = 'filename=%s.xls' % menu_date
    elif u'MSIE' in request.META['HTTP_USER_AGENT']:
        # IE does not support internationalized filename at all.
        # It can only recognize internationalized URL, so we do the trick via routing rules.
        filename_header = ''
    else:
        # For others like Firefox, we follow RFC2231 (encoding extension in HTTP headers).
        filename_header = 'filename*=UTF-8\'\'%s' % urllib.quote(menu_date.encode('utf-8'))
    response['Content-Disposition'] = 'attachment; ' + filename_header

    return response

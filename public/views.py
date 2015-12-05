# -*- coding: utf-8 -*-

import re
import os
# import mongoengine
from datetime import datetime
from datetime import timedelta
from collections import OrderedDict

import xlrd
import xlwt
from xlutils.copy import copy as xlcopy


import bson
import flask

from flask import Blueprint

from flask import request
from flask import send_from_directory
from flask import Response
# from flask import Flask, request, abort, Response, redirect, url_for, flash, Blueprint, send_from_directory
# from flask.ext.mongoengine import MongoEngine
from flask.templating import render_template
# from flask import make_response
from flask_security.decorators import roles_required
from flask_security.decorators import login_required
# from flask_security.decorators import roles_accepted

from flask import jsonify
from user.models import User
from flask.ext.security import current_user
from mongoengine.queryset import DoesNotExist

from werkzeug import secure_filename
from settings import Config
from public.models import Product
from public.models import Menu
from public.models import Category
from public.models import MenuProduct
from public.models import UserDocument
from public.models import ProductPositionsInXLS
from public.models import Order


bp_public = Blueprint('public', __name__, static_folder='../static')


def is_food_row(row):
    if isinstance(row[0].value, float):
        return True
    return False


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in Config.ALLOWED_EXTENSIONS


def add_products_from_xls(filename):
    rb = xlrd.open_workbook(filename, formatting_info=True)

    for sheet_index in xrange(5):
        sheet = rb.sheet_by_index(sheet_index)

        menu_date = re.findall(r'\d{2}.\d{2}.\d{2}', sheet.cell_value(0, 1)).pop()
        menu_date = datetime.strptime(menu_date, '%d.%m.%y')
        current_category = ''

        ud = UserDocument()
        ud.date = menu_date
        menu_file = open(filename, 'r')
        ud.contents.put(menu_file, content_type='application/vnd.ms-excel')
        try:
            ud.save()
        except flask.ext.mongoengine.mongoengine.NotUniqueError:
            pass

        try:
            menu = Menu(date=menu_date)
            menu.save()
        except flask.ext.mongoengine.mongoengine.NotUniqueError:
            menu = Menu.objects.get(date=menu_date)

        for rownum in range(sheet.nrows):
            rslc = sheet.row_slice(rownum)
            if is_food_row(rslc):
                try:
                    category = Category()
                    category.name = current_category
                    category.save()
                except flask.ext.mongoengine.mongoengine.NotUniqueError:
                    category = Category.objects.get(name=current_category)

                product = Product()
                product.name = unicode(rslc[1].value)

                weight = unicode(rslc[2].value).replace('.0', '').strip('-')
                if not weight:
                    # grammi
                    maybe_weight_is_here = re.findall(ur'([0-9,]+)(\W?\u0433\u0440)', product.name)
                    if len(maybe_weight_is_here) > 0:
                        pieces = re.findall(ur'\u043f\u043e\W*\d+\W*\u043f', product.name)
                        weight, description = maybe_weight_is_here.pop()
                        product.name = product.name.replace(weight + description, '')
                        weight = weight + u' \u0433'
                        weight = weight.replace(',', '.')
                        if len(pieces) > 0:
                            piece_part = u' (' + pieces.pop() + u')'
                            weight = weight + piece_part
                            product.name = product.name.replace(piece_part, '')

                    # shtuki
                    maybe_weight_is_here = re.findall(u'(\d+)(\W?\u0448\u0442)', product.name)
                    if len(maybe_weight_is_here) > 0:
                        weight, description = maybe_weight_is_here.pop()
                        product.name = product.name.replace(weight + description, '')
                        weight = weight + u' \u0448\u0442'

                    # kuski
                    maybe_weight_is_here = re.findall(u'(\d+)(\W?\u043a)', product.name)
                    if len(maybe_weight_is_here) > 0:
                        weight, description = maybe_weight_is_here.pop()
                        product.name = product.name.replace(weight + description, '')
                        weight = weight + u' \u043a'

                    # litry
                    maybe_weight_is_here = re.findall(u'([0-9,]+)(\W?\u043b)', product.name)
                    if len(maybe_weight_is_here) > 0:
                        weight, description = maybe_weight_is_here.pop()
                        product.name = product.name.replace(weight + description, '')
                        weight = weight + u' \u043b'
                        weight = weight.replace(',', '.')

                    # millylitry
                    maybe_weight_is_here = re.findall(u'([0-9,]+)(\W?\u043c\u043b)', product.name)
                    if len(maybe_weight_is_here) > 0:
                        weight, description = maybe_weight_is_here.pop()
                        product.name = product.name.replace(weight + description, '')
                        weight = weight + u' \u043c\u043b'
                        weight = weight.replace(',', '.')
                else:
                    weight = weight + u' \u0433'

                def chg_quotes(text=None):
                    if not text:
                        return
                    counter = 0
                    text = list(text)
                    for i in range(len(text)):
                        if (text[i] == u'"'):
                            counter += 1
                            if (counter % 2 == 1):
                                text[i] = u'«'
                            else:
                                text[i] = u'»'
                    return ''.join(text)

                weight = re.sub(u'(\w)(\u0448\u0442)', '\\1 \\2', weight)
                product.name = chg_quotes(product.name)
                replacements = {
                    r'\.': u'',
                    r',(\W)': u', \\1',
                    r'[,. ]+$': u'',
                    u'Шоколад «Аленка» с начинкой Вареная сгущенка': u'Шоколад «Алёнка» с варёной сгущёнкой',
                    u'Щи Щавелевые с яйцом': u'Щи щавелевые с яйцом',
                    u'Лапша Грибная домашняя': u'Лапша грибная домашняя',
                    u'Суп Фасолевый с говядиной': u'Суп фасолевый с говядиной',
                    u'Борщ «Украинский» с курицей': u'Борщ украинский с курицей',
                    u'Суп Рыбный': u'Суп рыбный',
                    u'ПАСТА Таглиателли с курицей в сырном соусе': u'Паста тальятелле с курицей в сырном соусе',
                    u'Лапша пшеничная удон с курицей, бульоном и яйцом': u'Лапша пшеничная удон (курица, бульон и яйцо)',
                }

                for was, then in replacements.iteritems():
                    product.name = re.sub(was, then, product.name)

                compounds = re.findall(r'\(\W+\)', product.name)
                if len(compounds) > 0:
                    compound = compounds.pop()
                    product.compound = re.sub(r'\((\W+)\)', '\\1', compound)
                    product.name = product.name.replace(compound, '')

                product.weight = weight
                product.cost = int(rslc[3].value)
                product.category = category

                try:
                    product.save()
                except flask.ext.mongoengine.mongoengine.NotUniqueError:
                    product = Product.objects.get(name=product.name,
                                                  weight=product.weight,
                                                  cost=product.cost)
                except bson.errors.InvalidBSON:
                    continue

                # saving product position
                ppix = ProductPositionsInXLS()
                ppix.product = product
                ppix.menu = menu
                ppix.row_in_xls = rownum
                try:
                    ppix.save()
                except flask.ext.mongoengine.mongoengine.NotUniqueError:
                    pass

                pmconnection = MenuProduct()
                pmconnection.menu = menu
                pmconnection.product = product
                try:
                    pmconnection.save()
                except flask.ext.mongoengine.mongoengine.NotUniqueError:
                    continue
            else:
                current_category = rslc[0].value
                replacements = {
                    u'ПЕРВЫЕ БЛЮДА': u'Первые блюда',
                    u'ВТОРЫЕ БЛЮДА': u'Вторые блюда',
                    u'САЛАТЫ ЗАПРАВЛЕННЫЕ  И ЗАКУСКИ': u'Салаты заправленные и закуски',
                    u'САЛАТЫ НЕ ЗАПРАВЛЕННЫЕ': u'Салаты незаправленные',
                    u'ЗАПРАВКИ К САЛАТАМ И СОУСЫ': u'Заправки к салатам и соуса',
                    u'ПИРОЖНОЕ': u'Пирожные',
                }
                for was, then in replacements.iteritems():
                    current_category = re.sub(was, then, current_category)


@bp_public.route('/index')
def index():
    return render_template('index.html')


@bp_public.route('/robots.txt')
def static_from_root():
    return send_from_directory(bp_public.static_folder, request.path[1:])


@bp_public.route('/order', methods=['POST'])
@login_required
def order():
    cuser = User.objects.get(id=current_user.id)
    product_id = request.values.get('product')
    menu_id = request.values.get('menu')

    try:
        menu = Menu.objects.get(id=menu_id)
    except DoesNotExist:
        pass

    try:
        product = Product.objects.get(id=product_id)
    except DoesNotExist:
        pass

    try:
        myorder = Order.objects.get(menu=menu, product=product, user=cuser)
        myorder.count += 1
        myorder.save()
    except DoesNotExist:
        myorder = Order()
        myorder.menu = menu
        myorder.product = product
        myorder.user = cuser
        myorder.save()

    myorders = Order.objects(menu=menu, user=cuser).values_list('product', 'count')
    mycosts = [(mt[0].cost, mt[1]) for mt in myorders]
    total = sum(mc[0]*mc[1] for mc in mycosts)
    allorders = Order.objects(menu=menu).values_list('product', 'count')
    allcosts = [(mt[0].cost, mt[1]) for mt in allorders]
    sum_order_cost = sum(mc[0]*mc[1] for mc in allcosts)

    rest = 1500 - sum_order_cost
    if rest < 0:
        rest = 0

    return jsonify(count=myorder.count,
                   name=product.name,
                   cost=product.cost,
                   menu=menu_id,
                   total=total,
                   sum_order_cost=sum_order_cost,
                   rest=rest)


@bp_public.route('/cancel', methods=['POST'])
@login_required
def cancel():
    cuser = User.objects.get(id=current_user.id)
    product_id = request.values.get('product')
    menu_id = request.values.get('menu')

    try:
        menu = Menu.objects.get(id=menu_id)
    except DoesNotExist:
        pass

    try:
        product = Product.objects.get(id=product_id)
    except DoesNotExist:
        pass

    try:
        order = Order.objects.get(menu=menu, product=product, user=cuser)
    except DoesNotExist:
        return jsonify(count=0,
                       name=product.name,
                       cost=0)

    if order.count > 1:
        order.count -= 1
        count = order.count
    else:
        count = 0
        order.delete()
    order.save()

    myorders = Order.objects(menu=menu, user=cuser).values_list('product', 'count')
    mycosts = [(mt[0].cost, mt[1]) for mt in myorders]
    total = sum(mc[0]*mc[1] for mc in mycosts)
    allorders = Order.objects(menu=menu).values_list('product', 'count')
    allcosts = [(mt[0].cost, mt[1]) for mt in allorders]
    sum_order_cost = sum(mc[0]*mc[1] for mc in allcosts)
    rest = 1500 - sum_order_cost
    if rest < 0:
        rest = 0

    return jsonify(count=count,
                   name=product.name,
                   cost=product.cost,
                   menu=menu_id,
                   total=total,
                   sum_order_cost=sum_order_cost,
                   rest=rest)


def get_prev_order_menu_date():
    now = datetime.today()

    if now.weekday() == 4:  # friday
        prev_date = datetime.today()
    elif now.weekday() == 5:  # saturday
        prev_date = datetime.today() - timedelta(days=1)
    elif now.weekday() == 6:  # sunday
        prev_date = datetime.today() - timedelta(days=2)
    else:  # weekdays
        if now.hour >= 15:
            prev_date = datetime.today() + timedelta(days=1)
        else:
            prev_date = datetime.today()

    return prev_date

def get_order_menu_date():
    now = datetime.today()

    if now.weekday() == 4:  # friday
        now = datetime.today() + timedelta(days=3)
    elif now.weekday() == 5:  # saturday
        now = datetime.today() + timedelta(days=2)
    elif now.weekday() == 6:  # sunday
        now = datetime.today() + timedelta(days=1)
    else:  # weekdays
        if now.hour >= 15:
            now = datetime.today() + timedelta(days=2)
        else:
            now = datetime.today() + timedelta(days=1)

    return now

def menu_date_format(menu_date):
    return '{year}-{month}-{day}'.format(year=menu_date.year,
                                         month=menu_date.month,
                                         day=menu_date.day)


@bp_public.route('/')
@login_required
def view_menu():
    user_email = request.values.get('ue')

    admin_error = ''
    if user_email:
        try:
            cuser = User.objects.get(email=user_email)
        except DoesNotExist:
            admin_error = 'unable to login with user {email}'.format(email=user_email)
            cuser = User.objects.get(id=current_user.id)
    else:
        cuser = User.objects.get(id=current_user.id)

    order_menu_date = get_order_menu_date()
    prev_order_menu_date = get_prev_order_menu_date()
    menu_date = menu_date_format(order_menu_date)
    prev_menu_date = menu_date_format(prev_order_menu_date)

    menu = Menu.objects(date=menu_date).first()
    prev_menu = Menu.objects(date=prev_menu_date).first()
    all_products = MenuProduct.objects.filter(menu=menu).values_list('product').all_fields()
    all_ordered_products = Order.objects.filter(product__in=all_products, menu=menu)
    ordered_products = Order.objects.filter(product__in=all_products, menu=menu, user=cuser).all_fields()
    users_ordered = len(set(all_ordered_products.values_list('user')))

    all_prev_products = MenuProduct.objects.filter(menu=prev_menu).values_list('product').all_fields()
    prev_orders = Order.objects.filter(product__in=all_prev_products, menu=prev_menu, user=cuser)

    prev_products = OrderedDict()
    prev_total_cost = 0
    for prev_order in prev_orders:
        prev_product = prev_order.product

        if not prev_products.get(prev_product.category.name):
            prev_products[prev_product.category.name] = []

        prev_total_cost += prev_product.cost*prev_order.count

        prev_products[prev_product.category.name].append({
            'id': prev_order.product.id,
            'category_id': prev_product.category.id,
            'name': prev_product.name,
            'weight': prev_product.weight,
            'cost': prev_product.cost*prev_order.count,
            'compound': prev_product.compound,
            'count': prev_order.count,
        })

    products = OrderedDict()
    for product in all_products:
        order_count = 0
        for order in ordered_products:
            if order.product == product:
                order_count = order.count
                break

        if not products.get(product.category.name):
            products[product.category.name] = []

        products[product.category.name].append({
            'id': product.id,
            'category_id': product.category.id,
            'name': product.name,
            'weight': product.weight,
            'cost': product.cost,
            'compound': product.compound,
            'count': order_count,
        })

    months = [u'января',
              u'февраля',
              u'марта',
              u'апреля',
              u'мая',
              u'июня',
              u'июля',
              u'августа',
              u'сентбяря',
              u'октября',
              u'ноября',
              u'декабря']

    weekdays = [u'понедельник',
                u'вторник',
                u'среду',
                u'четверг',
                u'пятницу',
                u'субботу',
                u'воскресение']

    if menu and products:
        myorders = Order.objects(menu=menu, user=cuser).values_list('product', 'count')
        mycosts = [(mt[0].cost, mt[1]) for mt in myorders]
        total = sum(mc[0]*mc[1] for mc in mycosts)
        allorders = Order.objects(menu=menu).values_list('product', 'count')
        allcosts = [(mt[0].cost, mt[1]) for mt in allorders]
        sum_order_cost = sum(mc[0]*mc[1] for mc in allcosts)

        rest = 1500 - sum_order_cost
        if rest < 0:
            rest = 0

        if sum_order_cost > 1500:
            delivery_cost = 0.0
            delivery_type = 'free'
        elif sum_order_cost > 1000:
            delivery_cost = 100.0
            delivery_type = 'cheap'
        else:
            delivery_cost = 200.0
            delivery_type = 'expensive'

        rest = 1500 - sum_order_cost
        if rest < 0:
            rest = 0

        return render_template('viewmenu.html',
                               products=products,
                               menu_id=menu.id,
                               menu_day=order_menu_date.day,
                               menu_weekday=weekdays[order_menu_date.weekday()],
                               menu_month=months[order_menu_date.month-1],
                               menu_year=order_menu_date.year,
                               total=total,
                               prev_products=prev_products,
                               prev_total_cost=prev_total_cost,
                               admin_error=admin_error,
                               sum_order_cost=sum_order_cost,
                               delivery_cost=delivery_cost,
                               delivery_type=delivery_type,
                               rest=rest,
                               users_ordered=users_ordered,
                               user_is_admin=current_user.has_role('admin'))
    else:
        return render_template('500.html'), 500


@bp_public.route('/loadmenu', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def load_menu():
    if request.method == 'GET':
        return render_template('loadmenu.html')
    elif request.method == 'POST':
        menu = request.files['menu']
        if menu and allowed_file(menu.filename):
            filename = secure_filename(menu.filename)
            path = os.path.join(Config.UPLOAD_FOLDER, filename)
            menu.save(path)

            try:
                add_products_from_xls(path)
            except IndexError:
                return render_template('loadmenu.html', status='error')
            return render_template('loadmenu.html', status='success')
        else:
            return render_template('loadmenu.html', status='error')


@bp_public.route('/getmenu', methods=['GET'])
@login_required
@roles_required('admin')
def get_menu():
    order_menu_date = get_order_menu_date()
    formatted_date = menu_date_format(order_menu_date)
    menu_xls = UserDocument.objects(date=formatted_date).first()
    xls_contents = menu_xls.contents.read()
    weekday = order_menu_date.weekday()

    tmp_filename = '/tmp/tmp.xls'
    tmp_xls = open(tmp_filename, 'w')
    tmp_xls.write(xls_contents)
    tmp_xls.close()

    read_book = xlrd.open_workbook(tmp_filename, on_demand=True, formatting_info=True)
    write_book = xlcopy(read_book)
    write_sheet = write_book.get_sheet(weekday)

    menu = Menu.objects(date=formatted_date).first()
    orders = Order.objects(menu=menu)
    ppixs = ProductPositionsInXLS.objects.filter(product__in=orders.values_list('product'), menu=menu)

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
    total_row_pos = ProductPositionsInXLS.objects.filter(menu=menu).order_by('-row_in_xls').first().row_in_xls + 1

    for ppix in ppixs:
        count = sum(order.count for order in orders.filter(product=ppix.product))
        cost = ppix.product.cost * count
        write_sheet.write(ppix.row_in_xls, 4, count, style=style)
        write_sheet.write(ppix.row_in_xls, 5, cost, style=style)
        total += cost

    write_sheet.write(total_row_pos, 5, total, style=total_cell_style)
    write_book.save(tmp_filename)

    return Response(open(tmp_filename, 'r'), content_type='application/vnd.ms-excel')

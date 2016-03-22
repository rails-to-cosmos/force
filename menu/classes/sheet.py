# -*- coding: utf-8 -*-
import re
import mmh3

from django.utils import timezone
from datetime import datetime
from product import Product


class Sheet(object):
    def __init__(self, xlsheet):
        self.xlsheet = xlsheet

    def parse_date(self):
        menu_date = re.findall(r'\d{2}.\d{2}.\d{2}',
                               self.xlsheet.cell_value(0, 1)).pop()
        current_tz = timezone.get_current_timezone()
        result_date = datetime.strptime(menu_date, '%d.%m.%y')
        result_date = current_tz.localize(result_date)
        return result_date

    def parse_products(self):
        category = ''
        products = list()
        for current_row_num in xrange(self.xlsheet.nrows):
            current_row = self.xlsheet.row_slice(current_row_num)
            if self.is_food_row(current_row):
                product = self.parse_product(current_row)
                product.category = category
                product.position = current_row_num
                products.append(product)
            else:
                category = self.parse_category(current_row)
                category = self.cleanup_category(category)
        return products

    def parse_product(self, row):
        product = Product()
        product.name, product.weight = self.parse_product_weight(row)
        product.name = self.change_quotes(product.name)
        product.name = self.cleanup_product_name(product.name)
        product.name, product.compound = self.parse_product_compound(product.name)
        product.name = product.name.strip()
        product.cost = self.parse_product_cost(row)
        product.name = re.sub(' +', ' ', product.name)
        product.hash = mmh3.hash(product.name.encode('utf-8') +
                                 product.compound.encode('utf-8') +
                                 product.weight.encode('utf-8'))
        return product

    def parse_category(self, row):
        return row[0].value

    def cleanup_category(self, category):
        replacements = {
            u'ПЕРВЫЕ БЛЮДА': u'Первые блюда',
            u'ВТОРЫЕ БЛЮДА': u'Вторые блюда',
            u'САЛАТЫ ЗАПРАВЛЕННЫЕ  И ЗАКУСКИ': u'Салаты заправленные и закуски',
            u'САЛАТЫ НЕ ЗАПРАВЛЕННЫЕ': u'Салаты незаправленные',
            u'ЗАПРАВКИ К САЛАТАМ И СОУСЫ': u'Заправки к салатам и соуса',
            u'ПИРОЖНОЕ': u'Пирожные',
        }
        for was, then in replacements.iteritems():
            category = re.sub(was, then, category)
        return category

    def parse_product_name(self, row):
        return unicode(row[1].value)

    def change_quotes(self, text):
        counter = 0
        text = list(text)
        for i, c in enumerate(text):
            if (c == u'"'):
                counter += 1
                if (counter % 2 == 1):
                    text[i] = u'«'
                else:
                    text[i] = u'»'
        return ''.join(text)

    def cleanup_product_name(self, product_name):
        clean_product_name = product_name

        replacements = {
            ur'\.': u'',
            ur',(\W)': u', \\1',
            ur'[,. ]+$': u'',
            ur'[ ]+': u' ',
            u'Шоколад «Аленка» с начинкой Вареная сгущенка': u'Шоколад «Алёнка» с варёной сгущёнкой',
            u'Щи Щавелевые с яйцом': u'Щи щавелевые с яйцом',
            u'Печень Куриная с жареным луком в сливочном соусе': u'Печень куриная с жареным луком в сливочном соусе',
            u'Лапша Грибная домашняя': u'Лапша грибная домашняя',
            u'Суп Фасолевый с говядиной': u'Суп фасолевый с говядиной',
            u'Борщ «Украинский» с курицей': u'Борщ украинский с курицей',
            u'Суп Рыбный': u'Суп рыбный',
            u'ПАСТА Таглиателли с курицей в сырном соусе': u'Паста тальятелле с курицей в сырном соусе',
            u'Лапша пшеничная удон с курицей, бульоном и яйцом': u'Лапша пшеничная удон (курица, бульон и яйцо)',
        }

        for was, then in replacements.iteritems():
            clean_product_name = re.sub(was, then, clean_product_name)

        return clean_product_name

    def parse_product_weight(self, row):
        product_name = self.parse_product_name(row)
        weight = unicode(row[2].value).replace('.0', '').strip('-')
        if weight:
            weight = weight + u' \u0433'
        else:
            parsing_attempts = [
                {
                    'name': 'grams',
                    'result': re.findall(ur'([0-9,]+)(\W?\u0433\u0440)', product_name),
                    'extension': u' \u0433'
                },
                {
                    'name': 'things',
                    'result': re.findall(ur'(\d+)(\W?\u0448\u0442)', product_name),
                    'extension': u' \u0448\u0442'
                },
                {
                    'name': 'flinders',
                    'result': re.findall(ur'(\d+)(\W?\u043a)', product_name),
                    'extension': u' \u043a'
                },
                {
                    'name': 'liters',
                    'result': re.findall(ur'([0-9,]+)(\W?\u043b)', product_name),
                    'extension': u' \u043b'
                },
                {
                    'name': 'milliliters',
                    'result': re.findall(ur'([0-9,]+)(\W?\u043c\u043b)', product_name),
                    'extension': u' \u043c\u043b'
                }
            ]

            for parsing_attempt in parsing_attempts:
                if parsing_attempt.get('result'):
                    weight, description = parsing_attempt.get('result').pop()
                    product_name = product_name.replace(weight + description, '')
                    weight = weight + parsing_attempt.get('extension')
                    weight = weight.replace(',', '.')
                    if parsing_attempt.get('name') == 'grams':
                        pieces = re.findall(ur'\u043f\u043e\W*\d+\W*\u043f', product_name)
                        if pieces:
                            piece_part = u' (' + pieces.pop() + u')'
                            weight = weight + piece_part
                            product_name = product_name.replace(piece_part, '')

        weight = re.sub(u'(\w)(\u0448\u0442)', '\\1 \\2', weight)
        return (product_name, weight)

    def parse_product_compound(self, product_name):
        compound = ''
        compounds = re.findall(r'\(\W+\)', product_name)
        if len(compounds) > 0:
            compound = compounds.pop()
            compound = re.sub(r'(\(\W+\))', '\\1', compound)
            product_name = product_name.replace(compound, '')
        return (product_name, compound)

    def parse_product_cost(self, row):
        return int(row[3].value)

    def is_food_row(self, row):
        return isinstance(row[0].value, float)

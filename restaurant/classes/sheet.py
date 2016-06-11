# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re

from django.utils import timezone
from datetime import datetime


class Sheet(object):
    def __init__(self, xlsheet):
        self.xlsheet = xlsheet

    def get_menu_date(self):
        menu_date = re.findall(r'\d{2}.\d{2}.\d{2}',
                               self.xlsheet.cell_value(0, 1)).pop()
        current_tz = timezone.get_current_timezone()
        unlocalized_date = datetime.strptime(menu_date, '%d.%m.%y')
        return current_tz.localize(unlocalized_date)

    def get_products(self):
        category = ''
        products = []

        for current_row_num in xrange(self.xlsheet.nrows):
            current_row = self.xlsheet.row_slice(current_row_num)

            if self.is_food_row(current_row):
                product = self.parse_product(current_row)
                product['category'] = category
                product['row'] = current_row_num
                products.append(product)
            else:
                category = self.parse_category(current_row)
                category = self.cleanup_category(category)

        return products

    def parse_product(self, row):
        name, weight = self.parse_weight(row)
        name = self.change_quotes(name)
        name = self.cleanup_product_name(name)
        name, compound = self.parse_product_compound(name)
        name = name.strip()
        product_cost = self.parse_product_cost(row)
        name = re.sub(' +', ' ', name)

        return {
            'name': name,
            'compound': compound,
            'weight': weight,
            'cost': product_cost
        }

    def parse_category(self, row):
        return row[0].value

    def cleanup_category(self, category):
        replacements = {
            'ПЕРВЫЕ БЛЮДА': 'Первые блюда',
            'ВТОРЫЕ БЛЮДА': 'Вторые блюда',
            'САЛАТЫ ЗАПРАВЛЕННЫЕ  И ЗАКУСКИ': 'Салаты заправленные и закуски',
            'САЛАТЫ НЕ ЗАПРАВЛЕННЫЕ': 'Салаты незаправленные',
            'ЗАПРАВКИ К САЛАТАМ И СОУСЫ': 'Заправки к салатам и соусы',
            'ПИРОЖНОЕ': 'Пирожные',
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
            if (c == '"'):
                counter += 1
                if (counter % 2 == 1):
                    text[i] = '«'
                else:
                    text[i] = '»'
        return ''.join(text)

    def cleanup_product_name(self, product_name):
        clean_product_name = product_name

        replacements = {
            r'\.': '',
            r',(\W)': ', \\1',
            r'[,. ]+$': '',
            r'[ ]+': ' ',
            'Шоколад «Аленка» с начинкой Вареная сгущенка': 'Шоколад «Алёнка» с варёной сгущёнкой',
            'Щи Щавелевые с яйцом': 'Щи щавелевые с яйцом',
            'Печень Куриная с жареным луком в сливочном соусе': 'Печень куриная с жареным луком в сливочном соусе',
            'Лапша Грибная домашняя': 'Лапша грибная домашняя',
            'Суп Фасолевый с говядиной': 'Суп фасолевый с говядиной',
            'Борщ «Украинский» с курицей': 'Борщ украинский с курицей',
            'Суп Рыбный': 'Суп рыбный',
            'ПАСТА Таглиателли с курицей в сырном соусе': 'Паста тальятелле с курицей в сырном соусе',
            'Лапша пшеничная удон с курицей, бульоном и яйцом': 'Лапша пшеничная удон (курица, бульон и яйцо)',
        }

        for was, then in replacements.iteritems():
            clean_product_name = re.sub(was, then, clean_product_name)

        return clean_product_name

    def parse_weight(self, row):
        product_name = self.parse_product_name(row)
        weight = unicode(row[2].value).replace('.0', '').strip('-')
        if weight:
            weight = weight + ' \u0433'
        else:
            parsing_attempts = [
                {
                    'name': 'grams',
                    'result': re.findall(ur'([0-9,]+)(\W?\u0433\u0440)', product_name),
                    'extension': ' \u0433'
                },
                {
                    'name': 'things',
                    'result': re.findall(ur'(\d+)(\W?\u0448\u0442)', product_name),
                    'extension': ' \u0448\u0442'
                },
                {
                    'name': 'flinders',
                    'result': re.findall(ur'(\d+)(\W?\u043a)', product_name),
                    'extension': ' \u043a'
                },
                {
                    'name': 'liters',
                    'result': re.findall(ur'([0-9,]+)(\W?\u043b)', product_name),
                    'extension': ' \u043b'
                },
                {
                    'name': 'milliliters',
                    'result': re.findall(ur'([0-9,]+)(\W?\u043c\u043b)', product_name),
                    'extension': ' \u043c\u043b'
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
                            piece_part = ' (' + pieces.pop() + ')'
                            weight = weight + piece_part
                            product_name = product_name.replace(piece_part, '')

        weight = re.sub('(\w)(\u0448\u0442)', '\\1 \\2', weight)
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

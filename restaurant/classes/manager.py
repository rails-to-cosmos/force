from __future__ import unicode_literals
from builtins import range

import xlrd
from sheet import Sheet


class MenuManager(object):
    def __init__(self):
        self.menus = {}

    def add_menus_from_file(self, filename):
        read_xls = xlrd.open_workbook(filename, formatting_info=True)
        for sheet_index in range(read_xls._all_sheets_count):
            sheet = Sheet(read_xls.sheet_by_index(sheet_index))
            try:
                date = sheet.get_menu_date()
                products = sheet.get_products()
            except IndexError:
                raise Exception('Invalid menu format!')
            self.menus[date] = products

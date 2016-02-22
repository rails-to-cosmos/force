import xlrd
from menu import Menu
from sheet import Sheet


class MenuManager(object):
    def __init__(self):
        self.menus = list()

    def add_menus_from_file(self, filename):
        read_xls = xlrd.open_workbook(filename, formatting_info=True)

        for sheet_index in xrange(read_xls._all_sheets_count):
            menu = Menu()
            sheet = Sheet(read_xls.sheet_by_index(sheet_index))
            menu.date = sheet.parse_date()
            menu.products = sheet.parse_products()
            self.menus.append(menu)

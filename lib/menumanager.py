import xlrd
from menu import Menu, MenuSheetMarking


class MenuManager(object):
    def __init__(self):
        self.menus = list()

    def add_menus_from_file(self, filename):
        read_xls = xlrd.open_workbook(filename, formatting_info=True)

        for sheet_index in xrange(read_xls._all_sheets_count):
            sheet = read_xls.sheet_by_index(sheet_index)
            menu = Menu()
            msm = MenuSheetMarking(sheet)
            menu.date = msm.parse_date()
            menu.products = msm.parse_products()
            self.menus.append(menu)

if __name__ == '__main__':
    mm = MenuManager()
    mm.add_menus_from_file('/Volumes/Main/Users/akatovda/Documents/Stuff/force/lib/menu.xls')

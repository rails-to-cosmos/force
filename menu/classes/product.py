class Product(object):
    def __init__(self):
        self.name = ''
        self.weight = ''
        self.compound = ''
        self.cost = ''
        self.category = ''
        self.position = 0
        self.menu = None
        self.obj = None

    def __repr__(self):
        return self.name.encode('utf-8')

from datetime import datetime
from extensions import db
from user.models import User


class Category(db.Document):
    name = db.StringField(required=True, unique=True)

    def __unicode__(self):
        return self.name


class Product(db.Document):
    name = db.StringField(required=True, unique_with=('cost', 'weight'))
    category = db.ReferenceField(Category)
    weight = db.StringField()
    compound = db.StringField()
    cost = db.IntField()

    def __unicode__(self):
        return self.name


class Menu(db.Document):
    date = db.DateTimeField(required=True, unique=True)


class MenuProduct(db.Document):
    menu = db.ReferenceField(Menu)
    product = db.ReferenceField(Product)


class Order(db.Document):
    menu = db.ReferenceField(Menu)
    product = db.ReferenceField(Product)
    user = db.ReferenceField(User)
    count = db.IntField(min_value=1, default=1)
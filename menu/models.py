from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Category(models.Model):
    name = models.CharField(max_length=255, blank=False, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'


class Product(models.Model):
    category = models.ForeignKey(Category)
    weight = models.CharField(max_length=255)
    compound = models.CharField(max_length=255)
    cost = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=255, blank=False)
    popularity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('name', 'cost')


class Menu(models.Model):
    date = models.DateTimeField('menu date')
    products = models.ManyToManyField(Product)

    def load(self):
        pass

    def view(self):
        pass


class Document(models.Model):
    date = models.DateTimeField('upload date', blank=False, unique=True)
    contents = models.FileField()


class ProductPositionsInXLS(models.Model):
    menu = models.ForeignKey(Menu)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    row_in_xls = models.PositiveIntegerField(blank=False)

    class Meta:
        unique_together = ('product', 'menu', 'row_in_xls')


class Order(models.Model):
    menu = models.ForeignKey(Menu)
    product = models.ForeignKey(Product)
    user = models.ForeignKey(User)
    count = models.PositiveIntegerField(validators=[MinValueValidator(1)],
                                        default=1)

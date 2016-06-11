from __future__ import unicode_literals

import mmh3

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Max


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def max_order():
        mo = Category.objects.values('order').aggregate(Max('order')).get('order__max') or 0
        return mo + 10

    order = models.IntegerField(default=max_order)

    def __repr__(self):
        return self.name

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    category = models.ForeignKey(Category)
    weight = models.CharField(max_length=255)
    compound = models.CharField(max_length=255, blank=True)
    cost = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=255)
    popularity = models.PositiveIntegerField(default=0, blank=True)
    added = models.DateTimeField(default=timezone.now)
    hash = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=1024, default='', blank=True)
    tags = models.CharField(max_length=1024, blank=True)

    def __unicode__(self):
        return self.name

    def added_fmt(self):
        return self.added.strftime('%d.%m.%Y')

    def category_name(self):
        return self.category.name

    @staticmethod
    def calculate_hash(name, compound, weight):
        return mmh3.hash(name.encode('utf-8') +
                         compound.encode('utf-8') +
                         weight.encode('utf-8'))


class Menu(models.Model):
    date = models.DateTimeField(default=timezone.now)
    products = models.ManyToManyField(Product)

    def __unicode__(self):
        return self.date.strftime('%d.%m.%Y')

    def date_fmt(self):
        return self.date.strftime('%d.%m.%Y')


class XLStructure(models.Model):
    menu = models.ForeignKey(Menu)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    position = models.PositiveIntegerField()

    class Meta:
        unique_together = ('product', 'menu', 'position')
        verbose_name = 'XLStructure'
        verbose_name_plural = 'XLStructures'


class Order(models.Model):
    menu = models.ForeignKey(Menu)
    product = models.ForeignKey(Product)
    user = models.ForeignKey(User, related_name='orders')
    count = models.PositiveIntegerField(default=1)
    date = models.DateTimeField(default=timezone.now)

from __future__ import unicode_literals

import mmh3

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Max

from db_file_storage.model_utils import delete_file, delete_file_if_needed



def max_order():
    mo = Category.objects.values('order').aggregate(Max('order')).get('order__max') or 0
    return mo + 10


class Category(models.Model):
    name = models.CharField(max_length=512, unique=True)

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
    added = models.DateField(default=timezone.now)
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


class MenuFile(models.Model):
    bytes = models.TextField()
    filename = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=50)


class Attachment(models.Model):
    menufile = models.FileField(upload_to='restaurant.MenuFile/bytes/filename/mimetype',
                            blank=False,
                            max_length=1024)
    upload_date = models.DateField(default=timezone.now)

    def save(self, *args, **kwargs):
        delete_file_if_needed(self, 'menufile')
        super(Attachment, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super(Attachment, self).delete(*args, **kwargs)
        delete_file(self, 'menufile')

    def __unicode__(self):
        return self.upload_date.strftime('%d.%m.%Y')


class Menu(models.Model):
    date = models.DateField(default=timezone.now)
    products = models.ManyToManyField(Product)
    attachment = models.ForeignKey(Attachment)

    def __unicode__(self):
        return self.date.strftime('%d.%m.%Y')

    def date_fmt(self):
        return self.date.strftime('%d.%m.%Y')

    @classmethod
    def get_current_menu(cls):
        return cls.objects.filter(date__gt=timezone.now()).order_by('date').first()


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

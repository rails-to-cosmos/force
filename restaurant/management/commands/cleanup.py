from django.db import connection
from django.core.management.base import BaseCommand, CommandError
from ...models import Product, Category, Menu, XLStructure, Order, Attachment

MODELS_TO_CLEANUP = [
    Product,
    Category,
    Menu,
    XLStructure,
    Order,
    Attachment
]


class Command(BaseCommand):
    help = 'Truncate menu tables.'

    def handle(self, *args, **options):
        cursor = connection.cursor()

        tables = [model._meta.db_table for model in MODELS_TO_CLEANUP]
        for table in tables:
            query = 'TRUNCATE {table} CASCADE'.format(table=table)
            cursor.execute(query)
            self.stdout.write(
                self.style.SUCCESS(
                    'Successfully truncated: %s' % query))

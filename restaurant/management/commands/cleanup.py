from django.db import connection
from django.core.management.base import BaseCommand, CommandError
from menu.models import Product, Category, Menu, XLStructure, Order


class Command(BaseCommand):
    help = 'Truncates menu tables'

    def handle(self, *args, **options):
        cursor = connection.cursor()
        models = [Product, Category, Menu, XLStructure, Order]
        tables = [model._meta.db_table for model in models]
        for table in tables:
            query = 'TRUNCATE {table} CASCADE'.format(table=table)
            cursor.execute(query)
        self.stdout.write(
            self.style.SUCCESS(
                'Successfully truncated: %s' % query))

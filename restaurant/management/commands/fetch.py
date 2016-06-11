from django.db import connection
from django.core.management.base import BaseCommand, CommandError
from menu.views import fetch_menu


class Command(BaseCommand):
    help = 'Downloads fresh menus'

    def handle(self, *args, **options):
        fetch_menu()
        self.stdout.write(self.style.SUCCESS('Successfully fetched'))

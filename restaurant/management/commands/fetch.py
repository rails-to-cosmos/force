from django.db import connection
from django.core.management.base import BaseCommand, CommandError
from ...views import fetch_menu


class Command(BaseCommand):
    help = 'Download fresh menus.'

    def handle(self, *args, **options):
        fetch_menu()
        self.stdout.write(self.style.SUCCESS('Successfully fetched'))

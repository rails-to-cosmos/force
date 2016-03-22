from django.contrib import admin

from models import (Provider,)


class ProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'urls', )


modules = ((Provider, ProviderAdmin),)
[admin.site.register(*module) for module in modules]

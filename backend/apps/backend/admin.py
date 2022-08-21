from django.contrib import admin

from backend.apps.backend.models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")

from django.contrib import admin
from .models import *


class ImageAdmin(admin.StackedInline):
    model = Image

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = [ImageAdmin]


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    pass


@admin.register(DailyMenu)
class DailyMenuAdmin(admin.ModelAdmin):
    #fieldsets = [
    #    (None, {
    #        "fields": [
    #            "name",
    #            "items"
    #            ]
    #        }
    #    ),
    #    ("Availability", {
    #        "fields": [
    #            "check_available", 
    #            "start_time", 
    #            "end_time"
    #            ]
    #        }
    #     ),
    #]
    def currently_available(self, obj):
        return obj.check_available()

@admin.register(WeeklyMenu)
class WeeklyMenuAdmin(admin.ModelAdmin):
    pass


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(ItemOrder)
class ItemOrderAdmin(admin.ModelAdmin):
    pass


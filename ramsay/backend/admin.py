from django.contrib import admin
from .models import *


#class ImageInLine(admin.StackedInline):
#    model = Image

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
   #inlines = [ImageInLine]
   pass

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
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


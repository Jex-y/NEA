from django.contrib import admin
from django import forms
from .models import *

"""
These are used to register the default admin interface for several models.
The defualt admin interface usally works well if the model is simple.

Meets requirements: 2.07
"""


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
   pass

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    pass

@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    pass

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    pass

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    pass

class ItemOrderInline(admin.TabularInline):
    """
    Used to show the item orders inline with with the relevant order so that they can be easily managed. 
    This allows an admin to add, remove or edit item orders in an order. 
    ...

    Attributes
    --------
    
    model : Model
        specifies the model that this admin from is for
    

    """
    model = Order.items.through

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ItemOrderInline
    ]
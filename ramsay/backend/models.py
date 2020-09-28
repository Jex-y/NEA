from django.db import models
from django.utils import timezone

class Item(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    price = models.FloatField()

class Menu(models.Model):
    name = models.CharField(max_length=64)
    items = models.ManyToManyField(Item)

    def __str__(self):
        return self.name

class DailyMenu(Menu):
    start_time = models.TimeField(blank=True)
    end_time = models.TimeField(blank=True)

    def check_available(self, time=None):
        import datetime
        if time is None:
            time = timezone.now().time()
        elif isinstance(time, datetime.datetime):
            time = time.time()

        return self.start_time <= time <= self.end_time

class Table(models.Model):
    table_number = models.IntegerField(primary_key=True)
            
class Order(models.Model):
    table = models.ForeignKey(Table, on_delete=models.PROTECT)
    items = models.ManyToManyField(
        Item,
        through="ItemOrder",
        through_fields=("order", "item")
    )


class ItemOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    notes = models.CharField(max_length=256)

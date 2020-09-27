from django.db import models
from django.utils import timezone

class Item(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    price = models.FloatField()

class Menu(models.Model):
    name = models.CharField(max_length=64)

    items = models.ManyToManyField(Item)

    start_time = models.TimeField(blank=True)
    end_time = models.TimeField(blank=True)
    reoccurs = models.CharField(max_length=2, choices=[
            ("DY", "daily"),
            ("WK", "weekly")
        ]
    )

    def check_available(self, time=None):
        import datetime

        if time is None:
            time = timezone.now()

        if self.reoccurs == "DY":
            today_start = self.start_time.replace(year=time.year, month=time.month, day=time.day)
            today_end = self.end_time.replace(year=time.year, month=time.month, day=time.day)
            result = today_start < time < today_end

        elif self.reoccurs == "WK":
            week_start = self.start_time.weekday()
            week_end = self.end_time.weekday()
            week_now = time.weekday()
            result = week_start <= week_end <= week_now

        else:
            result = True

        return result

    def __str__(self):
        return self.name

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

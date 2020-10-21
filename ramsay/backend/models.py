import uuid
import os
import datetime
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify  
from . import managers

class Tag(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=32)

    def get_upload_name(instance, filename):
        return "images/tags/{}.{}".format(instance.id,filename.split('.')[-1])

    icon = models.ImageField(upload_to=get_upload_name, blank=True, null=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256, blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    tags = models.ManyToManyField(Tag, blank=True)
    available = models.BooleanField(default=True)

    def get_upload_name(instance, filename):
        return "images/items/{}.{}".format(instance.id,filename.split('.')[-1])

    image = models.ImageField(upload_to=get_upload_name, blank=True, null=True)

    def __str__(self):
        return self.name

class Menu(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256, blank=True, null=True)
    items = models.ManyToManyField(Item)
    super_menu = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True)
    available = models.BooleanField(default=True)
    url_name = models.SlugField(max_length=64, editable=False)

    objects = managers.MenuManager()

    day_choices = [
            (0, "Monday"),
            (1, "Tuesday"),
            (2, "Wednesday"),
            (3, "Thursday"),
            (4, "Friday"),
            (5, "Saturday"),
            (6, "Sunday"),
        ]

    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    start_day = models.IntegerField(choices=day_choices, null=True, blank=True)
    end_day = models.IntegerField(choices=day_choices, null=True, blank=True)

    def get_upload_name(instance, filename):
        return "images/menus/{}.{}".format(instance.id,filename.split('.')[-1])

    image = models.ImageField(upload_to=get_upload_name, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.url_name = slugify(self.name)

        if isinstance(self.start_time, datetime.datetime):
            self.start_time = self.start_time.time()

        if isinstance(self.end_time, datetime.datetime):
            self.end_time = self.end_time.time()

        super(Menu, self).save(*args, **kwargs)

    def check_available(self, time=timezone.now()):
        """
        Could be made more efficent but is more clear this way.
        """
        if self.start_day is not None and self.end_day is not None: # Is weekly menu
            if self.start_time is not None and self.end_time is not None: # Has time constraint
                result = self.available and self.time_check_available(time) and self.week_check_available(time)
            else:
                result = self.available and self.week_check_available(time) # Has no time contstraint

        elif self.start_time is not None and self.end_time is not None: # Is daily menu
            result = self.available and self.time_check_available(time)

        else: # Is normal menu
            result = self.available
        return result

    def time_check_available(self, time):
        return self.start_time <= time.time() <= self.end_time

    def week_check_available(self, time):
        return self.start_day <= time.weekday() <= self.end_day

    def __str__(self):
        return self.name

class Table(models.Model):
    table_number = models.IntegerField(primary_key=True)

    def __str__(self):
        return f"Table {self.table_number}"
            
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
    notes = models.CharField(max_length=256, blank=True, null=True)

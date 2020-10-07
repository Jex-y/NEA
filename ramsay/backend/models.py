import uuid
import os
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify  


class Item(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    price = models.FloatField()
    
    def __str__(self):
        return self.name

class Image(models.Model):
    
    def get_upload_name(instance, filename):
        return "images/{}.{}".format(instance.id,filename.split('.')[-1])

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    image = models.ImageField(upload_to=get_upload_name)    
    item = models.OneToOneField(Item, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return os.path.join(settings.MEDIA_URI, self.image.url)

class Menu(models.Model):
    name = models.CharField(max_length=64)
    items = models.ManyToManyField(Item)
    super_menu = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True)
    available = models.BooleanField(default=True)
    url_name = models.SlugField(max_length=64, editable=False)

    def save(self, *args, **kwargs):
        self.url_name = slugify(self.name)
        super(Menu, self).save(*args, **kwargs)

    def check_available(self, *args, **kwargs):
        return self.available

    def __str__(self):
        return self.name

class DailyMenu(Menu):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def check_available(self, time=None):
        import datetime
        if time is None:
            time = timezone.now().time()
        elif isinstance(time, datetime.datetime):
            time = time.time()

        return (self.start_time <= time <= self.end_time) and self.available

    check_available.boolean = True

class WeeklyMenu(Menu):
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

    start_day = models.IntegerField(choices=day_choices)
    end_day = models.IntegerField(choices=day_choices)

    def check_available(self, time=None):
        import datetime
        if time is None:
            time = timezone.now()

        if self.start_time is not None and self.end_time is not None:
            time_result = self.start_time <= time.time() <= self.end_time
        else:
            time_result = True

        day_result = self.start_day <= time.weekday() <= self.end_day

        return time_result and day_result and self.available

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
    notes = models.CharField(max_length=256) # Make optional

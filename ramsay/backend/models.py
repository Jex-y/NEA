import uuid
import datetime
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify  

def get_upload_name(dir, instance, filename):
        """
        Passed to UploadField to get a path to store the file.

        File path is unqiue with the id attribute.

        Parameters:
            dir (str): directory to store image in
            instance (Model): instance of tag to create the file path for 
            filename (str): the filename of the uploded image. Used to get correct file extension.

            Returns:
                (str): relative filepath to save the icon image

        """
        return 'images/{}/{}.{}'.format(dir,instance.pk,filename.split('.')[-1])

def get_upload_name_tag(instance, filename):
    return get_upload_name('tags',instance,filename)

def get_upload_name_item(instance, filename):
    return get_upload_name('items',instance,filename)

def get_upload_name_menu(instance, filename):
    return get_upload_name('menus',instance,filename)

class Tag(models.Model):
    """
    A model to represent item tags 
    e.g. Vegan, Spicy, Alcoholic.
    Allows a user to filter on does or does not have a specific tag.
    Optionally has an icon that is shown next to the item on the menu.

    Meets requirements: 2.03
    ...

    Attributes
    --------
    id : UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
        primary key for database
    name : CharField(max_length=32)
        human readable name
    icon : ImageField(upload_to=self.get_upload_name, blank=True, null=True)
        icon displayed by item

    Methods
    --------

    __str__():
        Returns name.

    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=32)
    icon = models.ImageField(
        upload_to=get_upload_name_tag,
        blank=True, null=True)

    def __str__(self):
        """
        Returns name

        Parameters:
            None

        Returns:
            self.name (str): human readable name

        """
        return self.name

class Item(models.Model):
    """
    A model to represent an item.
    
    Meets requirements: 2.01
    ...

    Attributes
    --------
    id : UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
        primary key for database
    name : CharField(max_length=64) 
        human readable name
    description : CharField(max_length=256, blank=True, null=True)
        human readable description
    price : DecimalField(decimal_places=2, max_digits=6)
        the price of the item
    tags : ManyToManyField(Tag, blank=True)
        the tags assoiated with the item
    available : BooleanField(default=True)
        whether the item is currently available
        used to toggle if the item is available manually
    image : ImageField(upload_to=self.get_upload_name, blank=True, null=True)
        image showing the item

    Methods
    --------

    __str__():
        Returns name.

    """


    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256, blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    tags = models.ManyToManyField(Tag, blank=True)
    available = models.BooleanField(default=True)
    image = models.ImageField(
        upload_to=get_upload_name_item,
        blank=True, null=True)

    def __str__(self):
        """
        Returns name

        Parameters:
            None

        Returns:
            self.name (str): human readable name

        """
        return self.name


class Menu(models.Model):
    """
    A model to represent a menu.

    Meets requirements: 2.02
    ...

    Attributes
    --------
    id : UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
        primary key for database
    name : CharField(max_length=64)
        human readable name
    description : CharField(max_length=256, blank=True, null=True)
        human readable description
    items : ManyToManyField(Item)
        the items assosiated with the menu
    super_menu : ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
        foreign key to the menu that contains this menu
        used to create recurance relation needed for sub-menus
    available : BooleanField(default=True)
        whether the menu is currently available
        used to toggle if the menu is available manually
    url_name : SlugField(max_length=64, editable=False)
        url friendly string used to get the menu externally
    image: ImageField(upload_to=self.get_upload_name, blank=True, null=True)
        image showing the menu
    objects : MenuManager()
        used by the database managment to fetch from the database.
    day_choices : list(tuple(int, str))
        enumeration of the days of the week for dropdown menu in admin interface
    start_time : TimeField(null=True, blank=True)
        the first time that the menu is available each day
        used for menus that should only be available certain times of day
    end_time : TimeField(null=True, blank=True)
        the last time that the menu is available each day
        used for menus that should only be available certain times of day
    start_day : IntegerField(choices=day_choices, null=True, blank=True)
        the first day that the menu is available each week
        used for menus that should only be available certain days of the week
    end_day : IntegerField(choices=day_choices, null=True, blank=True)
        the last day that the menu is available each week
        used for menus that should only be available certain days of the week

    Methods
    --------

    save():
        Saves changes to the instance to the database.

    __str__():
        Returns name.

    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256, blank=True, null=True)
    items = models.ManyToManyField(Item, blank=True)
    super_menu = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    available = models.BooleanField(default=True)
    url_name = models.SlugField(max_length=64, editable=False)
    image = models.ImageField(
        upload_to=get_upload_name_menu,
        blank=True, null=True)

    day_choices = [
            (0, 'Monday'),
            (1, 'Tuesday'),
            (2, 'Wednesday'),
            (3, 'Thursday'),
            (4, 'Friday'),
            (5, 'Saturday'),
            (6, 'Sunday'),
        ]

    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    start_day = models.IntegerField(choices=day_choices, null=True, blank=True)
    end_day = models.IntegerField(choices=day_choices, null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Saves changes to the instance to the database.

        Parameters:
            None

        Returns:
            None

        """
        self.url_name = slugify(self.name)

        if isinstance(self.start_time, datetime.datetime):
            self.start_time = self.start_time.time()

        if isinstance(self.end_time, datetime.datetime):
            self.end_time = self.end_time.time()

        super(Menu, self).save(*args, **kwargs)

    def __str__(self):
        """
        Returns name

        Parameters:
            None

        Returns:
            self.name (str): human readable name

        """
        return self.name

class Table(models.Model):
    """
    A model to represent tables in a restaurant
    ...

    Attributes
    --------
    table_number : IntegerField(primary_key=True)
        the table number in the restaurant
        also the primary key in the database

    Methods
    --------

    __str__():
        Returns human readable string representing the table.

    """
    table_number = models.IntegerField(primary_key=True)

    def __str__(self):
        """
        Returns human readable string representing the table.

        Parameters:
            None

        Returns:
            (str): human readable string representing the table

        """
        return f'Table {self.table_number}'

class Session(models.Model):
    """
    A model to represent an open or closed session

    Meets requirements: 2.04 
    ...

    Attributes
    --------
    sessId : UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
        session ID, primary key for database
    table : ForeignKey(table, on_delete=models.PROTECT)
        foreign id to the table that the session is assoiated with
    start_time : DateTimeField(null=True, blank=True)
        the time that the session is started
    end_time : DateTimeField(null=True, blank=True)
        the time that the session is ended

    Methods
    --------
    None

    """
    sessId = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    table = models.ForeignKey(Table, on_delete=models.PROTECT)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)

            
class Order(models.Model):
    """
    A model to represent orders

    Meets requirements: 2.05
    ...

    Attributes
    --------
    session : ForeignKey(Session, on_delete=models.CASCADE)
        foreign key to the session that the order is assosiated with
    items : ManyToManyField(
        Item,
        through='ItemOrder',
        through_fields=('order', 'item')
    )
        the items assoiated with the order
        many to many through ItemOrder so that each item can have an assosiated quantity and notes
    submitted : models.DateTimeField(default=timezone.now)
        datetime that the order was submitted

    Methods
    --------
    None

    """
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    items = models.ManyToManyField(
        Item,
        through='ItemOrder',
        through_fields=('order', 'item'),
    )
    submitted = models.DateTimeField(default=timezone.now)

class ItemOrder(models.Model):
    """
    A model to create a many to many relationship with items and orders.
    Also records the quantity of items and any notes.

    Meets requirements: 2.06
    ...

    Attributes
    --------
    order : ForeignKey(Order, on_delete=models.CASCADE)
        foreign key to the order than the ItemOrder is a part of
    item : ForeignKey(Item, on_delete=models.CASCADE)
        foreign key to the item that the ItemOrder references
    quantity : IntegerField()
        the quantity of the item being ordered
    completed : models.BooleanField(default=False)
        whether the item order has been fulfilled
    notes : CharField(max_length=256, blank=True, null=True)
        any assosiated notes with the item order
        e.g. no gherkins 

    Methods
    --------
    None

    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    completed = models.BooleanField(default=False)
    notes = models.CharField(max_length=256, blank=True, null=True)


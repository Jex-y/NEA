import django
from django.test import TestCase
from backend.models import Item, Tag

class ItemTagFilterTest(TestCase):
    
    def setUp(self):
        self.tag1 = Tag(name='Tag1')
        self.tag2 = Tag(name='Tag2')

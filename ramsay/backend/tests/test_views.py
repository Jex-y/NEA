import django
from django.urls import reverse
from django.test import TestCase
from backend.models import Item, Tag
import json

class ItemSearchViewTest(TestCase):

    def setUp(self):
        self.apple = Item.objects.create(
            name='Apple', 
            description='Some text', 
            price=12.34)

        self.bannana = Item.objects.create(
            name='A name', 
            description='This is a bannana', 
            price=12.34)

    def test_full_name_search(self):
        expected = [{

            'id': str(self.apple.id),
            'name': 'Apple', 
            'description': 'Some text', 
            'price': '12.34', 
            'tags': [],
            'image': None
            }]

        response = self.client.get(reverse('backend:search',args=('apple',)))
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content)
        self.assertEqual(json_data, expected)

    def test_partial_name_search(self):
        expected = [{
            'id': str(self.apple.id),
            'name': 'Apple', 
            'description': 'Some text', 
            'price': '12.34', 
            'tags': [],
            'image': None
            }]

        response = self.client.get(reverse('backend:search',args=('ap',)))
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content)
        self.assertEqual(json_data, expected)

    def test_full_description_search(self):
        expected = [{
            'id': str(self.bannana.id),
            'name': 'A name', 
            'description': 'This is a bannana', 
            'price': '12.34',
            'tags': [],
            'image': None
            }]

        response = self.client.get(reverse('backend:search',args=('This is a bannana',)))
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content)
        self.assertEqual(json_data, expected)

    def test_partial_description_search(self):
        expected = [{
            'id': str(self.bannana.id),
            'name': 'A name', 
            'description': 'This is a bannana', 
            'price': '12.34',
            'tags': [],
            'image': None
            }]

        response = self.client.get(reverse('backend:search',args=('ba',)))
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content)
        self.assertEqual(json_data, expected)

    def test_no_results(self):
        expected = []

        response = self.client.get(reverse('backend:search',args=('carrot',)))
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content)
        self.assertEqual(json_data, expected)



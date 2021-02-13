import django
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from django.utils import timezone
from rest_framework import status
from backend.models import *
from backend.serializers import *
import json
import datetime

def checkJsonEqual(a, b):
    # Only needs to be used when the order of items may not be the same
    a = orderJson(a)
    b = orderJson(b)

    return a == b

def orderJson(data):
    if isinstance(data, dict):
        return sorted((key, orderJson(value)) for key, value in data.items())
    elif isinstance(data, list):
        return sorted(orderJson(x) for x in data)
    else:
        return data

class ItemSearchViewTest(APITestCase):

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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_data = json.loads(response.content)
        self.assertEqual(json_data, expected)

    def test_no_results(self):
        expected = []

        response = self.client.get(reverse('backend:search',args=('carrot',)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_data = json.loads(response.content)
        self.assertEqual(json_data, expected)

class ItemFilterViewTest(APITestCase):
    def setUp(self):
        self.tag1 = Tag.objects.create(name='tag1')
        self.tag2 = Tag.objects.create(name='tag2')
        self.tag3 = Tag.objects.create(name='tag3')

        self.apple = Item.objects.create(
            name='Apple', 
            description='Some text', 
            price=12.34)

        self.apple.tags.set([self.tag1, self.tag2])

        self.bannana = Item.objects.create(
            name='A name', 
            description='This is a bannana', 
            price=12.34)

        self.bannana.tags.set([self.tag1])

        self.coffee = Item.objects.create(
            name='Black coffee', 
            description='I need some of this right now it is like 2 AM and I am writing unit tests', 
            price=0.12)

    def test_one_tag_two_results(self):
        expected = ItemSerializer(
            [
                self.apple,
                self.bannana,
            ], 
            many=True).data
        
        tags = str(self.tag1.id)

        response = self.client.get(
            reverse('backend:filter', 
                args=(tags,)))
        
        self.assertTrue(
            checkJsonEqual(
                json.loads(response.content), 
                expected
            ))

    def test_one_tag_one_result(self):
        expected = ItemSerializer(
            [self.apple], 
            many=True).data
        
        tags = str(self.tag2.id)

        response = self.client.get(
            reverse('backend:filter', 
                args=(tags,)))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content), 
            expected)

    def test_two_tags(self):
        expected = ItemSerializer(
            [
                self.apple,
                self.bannana,
            ], 
            many=True).data
        
        tags = str(self.tag1.id) + '&' + str(self.tag2.id)

        response = self.client.get(
            reverse('backend:filter', 
                args=(tags,)))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            checkJsonEqual(
                json.loads(response.content), 
                expected
            ))

    def test_no_results(self):
        expected = ItemSerializer(
            [], 
            many=True).data
        
        tags = str(self.tag3.id)

        response = self.client.get(
            reverse('backend:filter', 
                args=(tags,)))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content), 
            expected)


    def test_empty_request(self):
        tags = ' '

        response = self.client.get(
            reverse('backend:filter', 
                args=(tags,)))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_request(self):
        tags = str(self.tag1.id) + '&' + str(self.tag2.id) + '&abcd1234' 
        
        response = self.client.get(
            reverse('backend:filter', 
                args=(tags,)))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        

class ItemDetailViewTest(APITestCase):

    def setUp(self):
        self.item1 = Item.objects.create(
            name='Apple', 
            description='Some text', 
            price=12.34)

    def test_valid(self):
        expected = {
            'id': str(self.item1.id),
            'name': 'Apple', 
            'description': 'Some text', 
            'price': '12.34',
            'tags': [],
            'image': None
            }

        response = self.client.get(
            reverse('backend:itemdetail',
            args=(self.item1.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_data = json.loads(response.content)
        self.assertEqual(json_data, expected)


class SessionCreateViewTest(APITestCase):

    def setUp(self):
        self.table1 = Table.objects.create(table_number=1)
        self.table2 = Table.objects.create(table_number=2)

    def test_valid(self):
        response = self.client.post(
            reverse('backend:newsess'),
            {'table_num':1},
            )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        json_data = json.loads(response.content)
        sessId = json_data['sessid']

        self.assertEqual(Session.objects.filter(sessId = sessId).count(), 1)
        self.assertEqual(Session.objects.get(sessId = sessId).table, self.table1)

    def test_invalid_arguments_empty(self):
        before_item_set = Session.objects.all()

        response = self.client.post(
            reverse('backend:newsess'),
            )


        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        after_item_set = Session.objects.all()

        self.assertQuerysetEqual(before_item_set, after_item_set)

    def test_invalid_arguments_format(self):
        before_item_set = Session.objects.all()

        response = self.client.post(
            reverse('backend:newsess'),
            {'table_num':'apples'},
            )


        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        after_item_set = Session.objects.all()

        self.assertQuerysetEqual(before_item_set, after_item_set)


    def test_table_already_taken(self):
        response = self.client.post(
            reverse('backend:newsess'),
            {'table_num':2},
            )

        json_data = json.loads(response.content)
        sessId = json_data['sessid']
        
        old_sess = Session.objects.get(sessId = sessId)
        

        response = self.client.post(
            reverse('backend:newsess'),
            {'table_num':2},
            )

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        
        new_sess = Session.objects.get(sessId = sessId)

        self.assertEqual(old_sess, new_sess)

    def test_table_does_not_exsist(self):
        before_item_set = Session.objects.all()

        response = self.client.post(
            reverse('backend:newsess'),
            {'table_num':3},
            )

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

        after_item_set = Session.objects.all()

        self.assertQuerysetEqual(before_item_set, after_item_set)


class SessionValidateTest(APITestCase):

    def setUp(self):
        table1 = Table.objects.create(table_number=1)

        self.valid_sess = Session.objects.create(
            table = table1
            )

    def test_valid(self):
        response = self.client.post(
            reverse('backend:validsess'),
            {'sessId':str(self.valid_sess.sessId)},
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_data = json.loads(response.content)
        self.assertTrue(json_data['valid'])

    def test_invalid_arguments_empty(self):
        response = self.client.post(
            reverse('backend:validsess'),
            )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        json_data = json.loads(response.content)
        self.assertFalse(json_data['valid'])


    def test_invalid_arguments_format(self):
        response = self.client.post(
            reverse('backend:validsess'),
            {'sessid':'This is an apple, not a uuid!'},
            )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        json_data = json.loads(response.content)
        self.assertFalse(json_data['valid'])

    def test_session_too_old(self):
        table2 = Table.objects.create(table_number=2)

        old_sess = Session.objects.create(
            table = table2,
            start_time = timezone.now() - datetime.timedelta(hours=13, seconds=1)
            )

        response = self.client.post(
            reverse('backend:validsess'),
            {'sessId':str(old_sess.sessId)},
            )

        self.assertEqual(response.status_code, status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE)
        json_data = json.loads(response.content)
        self.assertFalse(json_data['valid'])

    def test_session_in_future(self):
        table3 = Table.objects.create(table_number=3)

        future_sess = Session.objects.create(
            table = table3,
            start_time = timezone.now() + datetime.timedelta(hours=1)
            )

        response = self.client.post(
            reverse('backend:validsess'),
            {'sessId':str(future_sess.sessId)},
            )

        self.assertEqual(response.status_code, status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE)
        json_data = json.loads(response.content)
        self.assertFalse(json_data['valid'])

    def test_session_closed(self):
        table4 = Table.objects.create(table_number=4)

        closed_sess = Session.objects.create(
            table = table4,
            start_time = timezone.now() - datetime.timedelta(hours=1),
            end_time = timezone.now() - datetime.timedelta(seconds=1)
            )

        response = self.client.post(
            reverse('backend:validsess'),
            {'sessId':str(closed_sess.sessId)},
            )

        self.assertEqual(response.status_code, status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE)
        json_data = json.loads(response.content)
        self.assertFalse(json_data['valid'])

    def test_no_session(self):
        test_uuid = uuid.uuid4()
        # Make sure uuid is definitly not in database (shouldn't happend unless not truly random)
        while Session.objects.filter(sessId = test_uuid).count() > 0:
            test_uuid = uuid.uuid4()

        response = self.client.post(
            reverse('backend:validsess'),
            {'sessId':str(test_uuid)},
            )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        json_data = json.loads(response.content)
        self.assertFalse(json_data['valid'])


class OrderCreateTest(APITestCase):

    def setUp(self):
        table1 = Table.objects.create(table_number=1)
        self.sess = Session.objects.create(table=table1)


        self.apple = Item.objects.create(
            name='Apple', 
            description='Some text', 
            price=12.34)

        self.bannana = Item.objects.create(
            name='Bannan', 
            description='This is a bannana', 
            price=12.34)

    def test_valid(self):
        json_data = {
                'sessId':str(self.sess.sessId),
                'order': {
                    'items': {
                        str(self.apple.id): 4,
                        str(self.bannana.id) : 3,
                        },
                    'notes': 'I would like the apple sliced please',
                    },
                }

        response = self.client.post(reverse('backend:neworder'),json.dumps(json_data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        orders = Order.objects.filter(session=self.sess)

        self.assertEqual(orders.count(), 1)

        order = orders[0]

        self.assertEqual(order.notes, json_data['order']['notes'])
        self.assertEqual(order.items.count(), len(json_data['order']['items']))

        self.assertEqual(order.items.all()[0], self.apple)
        self.assertEqual(order.items.all()[1], self.bannana)
        
        self.assertEqual(ItemOrder.objects.all().count(), 2)

        self.assertIn(
                ItemOrder.objects.create(
                order=order,
                item=self.apple,
                quantity=json_data['order']['items'][str(self.apple.id)]
            ),
            ItemOrder.objects.all())

        self.assertIn(
                ItemOrder.objects.create(
                order=order,
                item=self.bannana,
                quantity=json_data['order']['items'][str(self.bannana.id)]
            ),
            ItemOrder.objects.all())

    def test_empty_order(self):
        json_data = {
                'sessId':str(self.sess.sessId),
                'order': {
                    'items': {},
                    'notes': 'I would like the apple sliced please',
                    },
                }

        response = self.client.post(reverse('backend:neworder'),json.dumps(json_data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

        orders = Order.objects.filter(session=self.sess)

        self.assertEqual(orders.count(), 0)

        self.assertEqual(ItemOrder.objects.all().count(), 0)

    def test_invalid_json(self):
        json_data = {
                'key':'value',
                'json_status': 'wrong',
                }

        response = self.client.post(reverse('backend:neworder'),json.dumps(json_data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        orders = Order.objects.filter(session=self.sess)

        self.assertEqual(orders.count(), 0)

        self.assertEqual(ItemOrder.objects.all().count(), 0)

    def test_invalid_sessid(self):
        json_data = {
                'sessId':'abcd1234',
                'order': {
                    'items': {
                        str(self.apple.id): 4,
                        str(self.bannana.id) : 3,
                        },
                    'notes': 'I would like the apple sliced please',
                    },
                }

        response = self.client.post(reverse('backend:neworder'),json.dumps(json_data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        orders = Order.objects.filter(session=self.sess)

        self.assertEqual(orders.count(), 0)

        self.assertEqual(ItemOrder.objects.all().count(), 0)

    def test_null_notes(self):
        json_data = {
                'sessId':str(self.sess.sessId),
                'order': {
                    'items': {
                        str(self.apple.id): 4,
                        str(self.bannana.id) : 3,
                        },
                    'notes': None,
                    },
                }

        response = self.client.post(reverse('backend:neworder'),json.dumps(json_data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        orders = Order.objects.filter(session=self.sess)

        self.assertEqual(orders.count(), 1)

        order = orders[0]

        self.assertEqual(order.notes, json_data['order']['notes'])
        self.assertEqual(order.items.count(), len(json_data['order']['items']))

        self.assertEqual(order.items.all()[0], self.apple)
        self.assertEqual(order.items.all()[1], self.bannana)
        
        self.assertEqual(ItemOrder.objects.all().count(), 2)

        self.assertIn(
                ItemOrder.objects.create(
                order=order,
                item=self.apple,
                quantity=json_data['order']['items'][str(self.apple.id)]
            ),
            ItemOrder.objects.all())

        self.assertIn(
                ItemOrder.objects.create(
                order=order,
                item=self.bannana,
                quantity=json_data['order']['items'][str(self.bannana.id)]
            ),
            ItemOrder.objects.all())
        

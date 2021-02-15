import datetime
import uuid
from django.http import Http404
from django.db.models import Q
from django.utils import timezone
from django.core import exceptions
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from . import models
from . import serializers


class ItemSearchView(APIView):

    def get_objects(self, query):
        try:
            return models.Item.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        except:
            raise Http404

    def get(self, request, query):
        items = self.get_objects(query)
        serializer = serializers.ItemSerializer(items, many=True, context={'request': request})
        return Response(serializer.data)

class ItemFilterView(APIView):

    def get_objects(self, tags):
        try:
            query = Q()
            # Returns matches for any of the tags
            for tag in tags:
                query = query | Q(tags__id=tag)

            itemSet = set(models.Item.objects.filter(query))
            # Set removes duplicates
            return itemSet
        except:
            raise Http404 # Something was wrong with the query

    def get(self, request, tags=None):
        items = self.get_objects(tags.split('&'))
        serializer = serializers.ItemSerializer(items, many=True, context={'request': request})
        return Response(serializer.data)

class ItemMenuListView(APIView):

    def get_objects(self, url_name):
        try:
            menus = models.Menu.objects.filter(url_name=url_name)
            item_queryset = models.Item.objects.none()
            submenu_queryset = models.Menu.objects.none()
            for menu in menus:
                if menu.check_available():
                    item_queryset |= menu.items.filter(available=True)
                    submenu_queryset |= models.Menu.objects.filter(super_menu=menu)
            return item_queryset, submenu_queryset
        except Exception as e:
            raise Http404

    def get_top_level(self):
        try:
            return models.Menu.objects.filter(super_menu=None)
        except:
            raise Http404
        
    def get(self, request, url_name=None):
        if url_name:
            items, menus = self.get_objects(url_name)
            item_serializer = serializers.ItemSerializer(items, many=True, context={'request': request})
            menu_serializer = serializers.MenuSerializer(menus, many=True, context={'request': request})
            data = {
                'items': item_serializer.data,
                'menus': menu_serializer.data,
                }
        else: # Top level
            menus = self.get_top_level()
            serializer = serializers.MenuSerializer(menus, many=True, context={'request': request})
            data = {
                'items': [],
                'menus': serializer.data
                }
        
        return Response(data)

class ItemDetailView(APIView):

    def get_objects(self, item_id):
        try:
            item = models.Item.objects.get(id=item_id)
            return item
        except Exception as e:
            raise Http404

    def get(self, request, item_id):
        item = self.get_objects(item_id)
        serializer = serializers.ItemSerializer(item, context={'request': request})
        return Response(serializer.data)

class SessionCreateView(APIView):

    def post(self, request):
        table_num = request.POST.get('table_num')

        try:
            table_num = int(table_num)
        except:
            table_num = None

        if not table_num:
            data = {
                'result':'Error: Parametrs not understood',
                'sessid':None,
                }

            requestStatus = status.HTTP_400_BAD_REQUEST

        elif models.Session.objects.filter(table=table_num, end_time=None).count() > 0:
            data = {
                'info':'Error: Open session already exsists for that table',
                'sessid':None,
                }

            requestStatus = status.HTTP_409_CONFLICT

        else:
            try:
                table = models.Table.objects.get(table_number = table_num)

                sess = models.Session.objects.create(table=table)

                data = {
                    'info':'Session created',
                    'sessid':sess.sessId,
                    }

                requestStatus = status.HTTP_201_CREATED
            except:
                data = {
                    'info':f'Error: table with number {table_num} does not exist',
                    'sessid':None
                    }

                requestStatus = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(data, requestStatus)

class SessionValidateView(APIView):

    def valid_uuidV4(self, value):
        value = str(value)
        try:
            test_uuid = uuid.UUID(value, version=4)
            assert(str(test_uuid) == value)
            result = True
        except (ValueError, AssertionError):
            result = False
        return result
    
    def post(self, request):
        # TODO: Check tables aswell?
        
        valid = False
        msg = 'Request format incorrect'
        requestStatus = status.HTTP_400_BAD_REQUEST
        sessId = request.POST.get('sessId')

        if self.valid_uuidV4(sessId):
            try:
                sess = models.Session.objects.get(sessId=sessId)
                if sess.start_time <= timezone.now() and sess.end_time is None and not (sess.start_time <= timezone.now() - datetime.timedelta(hours=12)):
                    # Check that start time is before now, session has not been closed and the session has not been opened more than 12 hours ago
                    msg = 'Session valid'
                    valid = True
                    requestStatus = status.HTTP_200_OK
                else:
                    msg = 'Session time invalid'
                    requestStatus = status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE

            except exceptions.ObjectDoesNotExist:
                msg = f'No session with sessId={sessId} found in database'
                requestStatus = status.HTTP_404_NOT_FOUND

        data = {
            'info': msg,
            'valid':valid,
            }

        return Response(data, requestStatus)

class OrderCreateView(APIView):

    def validate_json(self,json):
        try:
            sessid = json['sessId']
            items = json['order']['items']
            valid = True
        except KeyError:
            valid = False
        return valid


    def post(self, request):
        json = request.data

        requestStatus = status.HTTP_400_BAD_REQUEST

        if self.validate_json(json):
            try:
                if len(json['order']['items']) == 0:
                    requestStatus = status.HTTP_406_NOT_ACCEPTABLE

                else:
                    order = models.Order.objects.create(
                        session=models.Session.objects.get(sessId=json['sessId']))

                    for item in json['order']['items']:
                        num = json['order']['items'][item]['num']
                        notes = json['order']['items'][item]['notes']
                        itemOrder = models.ItemOrder.objects.create(
                            order=order,
                            item=models.Item.objects.get(id=item),
                            quantity=num,
                            notes=notes,
                            )
                    requestStatus = status.HTTP_204_NO_CONTENT

            except (exceptions.ObjectDoesNotExist, exceptions.ValidationError):
                requestStatus = status.HTTP_400_BAD_REQUEST

        return Response(status=requestStatus)

class TagListView(APIView):
    
    def get_objects(self):
        try:
            tags = models.Tag.objects.all()
            # TODO: Could fliter by if referenced by any items
            return tags
        except:
            raise Http404

    def get(self, request):
        tags = self.get_objects()
        serializer = serializers.TagSerializer(tags, many=True, context={'request': request})
        return Response(serializer.data)

class ItemOrderListView(APIView):
    def query_database(self):
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT backend_itemorder.id, name, quantity, notes FROM backend_item, backend_itemorder, backend_order WHERE
	            completed = false AND
	            backend_item.id = backend_itemorder.item_id AND
	            backend_order.id = backend_itemorder.order_id 
	            ORDER BY backend_order.submitted
            """)
            rows = cursor.fetchall()
            return rows

    def get(self, request):
        itemOrders = self.query_database()
        data = []
        for id, name, quantity, notes in itemOrders:
            data.append({
                        'id':str(uuid.UUID(id)),
                        'name':name,
                         'quantity':quantity,
                         'notes':notes,
                         })
        return Response(data)

class ItemOrderCompleteView(APIView):
    def post(self, request):
        id = request.data['id']
        requestStatus = status.HTTP_400_BAD_REQUEST
        try:
            itemOrder = models.ItemOrder.objects.get(id=id)
            itemOrder.completed = True
            itemOrder.save()
            requestStatus = status.HTTP_202_ACCEPTED
        except (exceptions.ObjectDoesNotExist, exceptions.ValidationError):
            requestStatus = status.HTTP_400_BAD_REQUEST

        return Response(status=requestStatus)

class SessionOrderListView(APIView):
    def get_objects(self, sessId):
        itemOrders = models.ItemOrder.object.filter(order__session=sessId)
        return itemOrders

    def get(self, request, sessId):
        itemOrders = self.get_objects(sessId)
        serializer = serializers.ItemOrderSerializer(itemOrders, many=True)
        return Response(serializer.data)

               
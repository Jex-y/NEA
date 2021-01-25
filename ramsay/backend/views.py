import datetime
import uuid
from django.http import Http404
from django.db.models import Q
from django.utils import timezone
from django.core import exceptions
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

    def get(self, request, query, format=None):
        items = self.get_objects(query)
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
                    item_queryset = item_queryset.union(menu.items.filter(available=True))
                    submenu_queryset = submenu_queryset.union(models.Menu.objects.filter(super_menu=menu))
            return item_queryset, submenu_queryset
        except Exception as e:
            raise Http404

    def get_top_level(self):
        try:
            return models.Menu.objects.filter(super_menu=None)
        except:
            raise Http404

    def get(self, request, url_name=None, format=None):
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

class SessionCreateView(APIView):

    def post(self, request, format=None):
        table_num = request.POST.get('table_num')

        try:
            table_num = int(table_num)
        except:
            table_num = None

        if not table_num:
            data = {
                "result":"Error: Parametrs not understood",
                "sessid":None,
                }

            requestStatus = status.HTTP_400_BAD_REQUEST

        elif models.Session.objects.filter(table=table_num, end_time=None).count() > 0:
            data = {
                "info":"Error: Open session already exsists for that table",
                "sessid":None,
                }

            requestStatus = status.HTTP_409_CONFLICT

        else:
            try:
                table = models.Table.objects.get(table_number = table_num)

                sess = models.Session.objects.create(table=table)

                data = {
                    "info":"Session created",
                    "sessid":sess.sessId,
                    }

                requestStatus = status.HTTP_201_CREATED
            except:
                data = {
                    "info":f"Error: table with number {table_num} does not exist",
                    "sessid":None
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
    
    def post(self, request, format=None):
        # TODO: Check tables aswell?
        
        valid = False
        msg = "Request format incorrect"
        requestStatus = status.HTTP_400_BAD_REQUEST
        sessId = request.POST.get('sessid')

        if self.valid_uuidV4(sessId):
            try:
                sess = models.Session.objects.get(sessId=sessId)
                if sess.start_time <= timezone.now() and sess.end_time is None and not (sess.start_time <= timezone.now() - datetime.timedelta(hours=12)):
                    # Check that start time is before now, session has not been closed and the session has not been opened more than 12 hours ago
                    msg = "Session valid"
                    valid = True
                    requestStatus = status.HTTP_200_OK
                else:
                    msg = "Session time invalid"
                    requestStatus = status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE

            except exceptions.ObjectDoesNotExist:
                msg = f"No session with sessId={sessId} found in database"
                requestStatus = status.HTTP_404_NOT_FOUND

        data = {
            "info": msg,
            "valid":valid,
            }

        return Response(data, requestStatus)

        


               
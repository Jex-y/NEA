from django.http import Http404
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from . import models
from . import serializers

class ItemDetailView(APIView):

    def get_object(self, id):
        try:
            return models.Item.objects.get(id=id)
        except:
            raise Http404

    def get(self, request, id, format=None):
        item = self.get_object(id)
        serializer = serializers.ItemSerializer(item, context={'request': request})
        return Response(serializer.data)

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

    def get(self, request, url_name, format=None):
        items, menus = self.get_objects(url_name)
        item_serializer = serializers.ItemSerializer(items, many=True, context={'request': request})
        menu_serializer = serializers.MenuSerializer(menus, many=True, context={'request': request})
        data = {
            'items': item_serializer.data,
            'menus': menu_serializer.data,
            }
        return Response(data)

class MenuListView(APIView):

    def get_objects(self):
        try:
            return models.Menu.objects.filter(super_menu=None)
        except:
            raise Http404

    def get(self, request, format=None):
        items = self.get_objects()
        serializer = serializers.MenuSerializer(items, many=True, context={'request': request})
        return Response(serializer.data)


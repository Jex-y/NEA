from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from . import models
from . import serializers

class ItemDetailView(APIView):

    def get_object(self, pk):
        try:
            return models.Item.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = serializers.ItemSerializer(item)
        return Response(serializer.data)


class ItemMenuListView(APIView):

    def get_objects(self, url_name):
        try:
            menus = models.Menu.objects.filter(url_name=url_name, super_menu=None)
            item_queryset = models.Item.objects.none()
            for menu in menus:
                # Test with times 
                if menu.check_available():
                    item_queryset = item_queryset.union(menu.items.all())
            return item_queryset
        except:
            raise Http404

    def get(self, request, url_name, format=None):
        items = self.get_objects(url_name)
        serializer = serializers.ItemSerializer(items, many=True)
        return Response(serializer.data)


class MenuListView(APIView):

    def get_objects(self):
        try:
            return models.Menu.objects.all()
        except:
            raise Http404

    def get(self, request, format=None):
        items = self.get_objects()
        serializer = serializers.MenuSerializer(items, many=True)
        return Response(serializer.data)


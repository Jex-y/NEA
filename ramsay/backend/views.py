from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from . import models
from . import serializers

class ItemDetail(APIView):

    def get_object(self, pk):
        try:
            return models.Item.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = serializers.ItemSerializer(item)
        return Response(serializer.data)


class ItemMenuList(APIView):

    def get_objects(self, menu):
        try:
            return models.Item.objects.get(menu=menu)
        except:
            raise Http404

    def get(self, request, menu, format=None):
        items = self.get_objects(menu)

        # Serialise items and return

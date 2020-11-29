from rest_framework import serializers
from .models import *

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'icon')

class ItemSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Item
        fields = ('id', 'name', 'description', 'price', 'tags', 'image')

class MenuSerializer(serializers.ModelSerializer):
   class Meta:
        model = Menu
        fields = ('name', 'url_name', 'description', 'image')


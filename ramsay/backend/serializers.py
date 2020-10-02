from rest_framework import serializers
from .models import *

class ItemSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=64)
    description = serializers.CharField(max_length=256)
    price = serializers.FloatField()
    image = serializers.CharField(max_length=256)

    def create(self, validated_data):
        return Snippet.objects.create(**validated_data)

    def get_image(self, obj):
        return obj.image.url

    def update():
        pass

    #TODO: Make serialiser for Item so that the image path is correct.



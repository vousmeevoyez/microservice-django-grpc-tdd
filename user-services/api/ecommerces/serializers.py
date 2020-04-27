"""
    Serializers
    _____________________
"""
from rest_framework.serializers import (ModelSerializer)
from api.ecommerces.models import Platform, Store, StorePlatform


class PlatformSerializer(ModelSerializer):

    class Meta:
        model = Platform
        fields = "__all__"


class StorePlatformSerializer(ModelSerializer):

    platform = PlatformSerializer()

    class Meta:
        model = StorePlatform
        fields = "__all__"

class StoreSerializer(ModelSerializer):

    store_platforms = StorePlatformSerializer(many=True)

    class Meta:
        model = Store
        fields = "__all__"

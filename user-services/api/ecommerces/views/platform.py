"""
    Platform Views
"""
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_202_ACCEPTED
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from api.ecommerces.models import Platform, Store
from api.ecommerces.serializers import (PlatformSerializer, StoreSerializer,
                                        StorePlatformSerializer)

from api.utils.reusable.serializers import UserOwnViewSet


class PlatformViewSet(ModelViewSet):
    """
        GET POST PUT PATCH DELETE /platforms/
        _____________________
        handle basic crud for platform model
    """
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer


class StoreViewSet(UserOwnViewSet):
    """
        GET POST PUT PATCH DELETE /stores/
        _____________________
        handle basic crud for Store model
    """
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

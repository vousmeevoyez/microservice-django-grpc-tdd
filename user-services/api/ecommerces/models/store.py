"""
    Store Platform Models
    ___________________
"""
from django.contrib.auth import get_user_model
from django.db.models import (CASCADE, Model, CharField, ForeignKey,
                              BooleanField)
from api.utils.reusable import BaseModel

user = get_user_model()


class Platform(Model):
    """
        Represent Available ecommerce platform
    """
    key = CharField(max_length=255)
    description = CharField(max_length=255)
    is_active = BooleanField(default=True)


class Store(BaseModel):
    """
        Represent Store that owned by user
    """
    user = ForeignKey(user, on_delete=CASCADE, related_name="stores")
    name = CharField(max_length=255)


class StorePlatform(BaseModel):
    """
        Represent Platform that Store connected to
    """
    store = ForeignKey(Store, on_delete=CASCADE, related_name="store_platforms")
    platform = ForeignKey(Platform, on_delete=CASCADE)


class Credential(Model):
    """
        Represent Ecommerce Credential
    """
    user = ForeignKey(user, on_delete=CASCADE, related_name="credentials")
    username = CharField(max_length=255)
    password = CharField(max_length=255)
    platform = ForeignKey(StorePlatform, on_delete=CASCADE, related_name="platform_credentials")
    is_active = BooleanField(default=True)

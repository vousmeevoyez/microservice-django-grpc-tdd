"""
    Device Models
    __________________
"""
from django.contrib.auth import get_user_model
from django.db.models import CASCADE, Model, CharField, ForeignKey
from api.utils.reusable import BaseModel

user = get_user_model()


class Device(BaseModel):
    """
        Represent Device that used by user
    """

    user = ForeignKey(user, on_delete=CASCADE, related_name="devices")
    platform = CharField(max_length=30)
    device_id = CharField(max_length=255)

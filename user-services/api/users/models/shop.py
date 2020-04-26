"""
    Shop Models
    ___________________
"""
from django.contrib.auth import get_user_model
from django.db.models import (
    CASCADE,
    Model,
    CharField,
    ForeignKey
)
from api.utils.reusable import BaseModel

user = get_user_model()

class Shop(BaseModel):
    """
        Represent Shop that owned by user
    """
    user = ForeignKey(user, on_delete=CASCADE, related_name="shops")
    name = CharField(max_length=255)

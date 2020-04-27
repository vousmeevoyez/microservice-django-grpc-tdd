from uuid import uuid4
from django.db.models import Model, UUIDField, BooleanField, DateTimeField


class BaseModel(Model):
    """ Extend django base user and common fields here """

    id = UUIDField(primary_key=True, default=uuid4)
    is_active = BooleanField(default=True)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

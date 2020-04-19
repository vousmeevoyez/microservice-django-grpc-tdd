from django.db.models import (Model, CASCADE, SET_NULL, CharField,
                              DateTimeField, EmailField, URLField, ImageField,
                              BooleanField, DecimalField, UUIDField,
                              IntegerField)

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .base import BaseModel

USER_TYPES = (("MERCHANT", "Merchant"), ("ADMIN", "Admin"))


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
            Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    """ Extend django base user and add user_type """
    username = CharField(max_length=100, unique=True)
    email = EmailField(unique=True)
    phone_ext = CharField(max_length=3, blank=True)
    phone_no = CharField(max_length=16, unique=True, blank=True)
    first_name = CharField(max_length=100, blank=True)
    middle_name = CharField(max_length=100, blank=True)
    last_name = CharField(max_length=100, blank=True)
    user_type = CharField(choices=USER_TYPES,
                          default=USER_TYPES[0][0],
                          max_length=32)
    is_staff = BooleanField(default=False)
    is_active = BooleanField(default=False)
    consumer_id = UUIDField(null=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["phone_ext", "phone_no", "first_name", "last_name"]

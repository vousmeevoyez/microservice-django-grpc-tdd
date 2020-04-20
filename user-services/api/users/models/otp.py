"""
    OTP Models
    __________________
"""
from math import floor
from random import random
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db.models import (CASCADE, BooleanField, CharField, DateTimeField,
                              ForeignKey)
from api.users.models.base import BaseModel
from api.users.choices import OTP_TYPES

User = get_user_model()


class Otp(BaseModel):
    """
        Represent OTP that triggered by user
    """
    user = ForeignKey(User, on_delete=CASCADE, related_name="otps")
    otp_type = CharField(choices=OTP_TYPES, max_length=100)
    code = CharField(max_length=255)
    valid_until = DateTimeField()
    is_verified = BooleanField(default=False)

    def _generate_code(self, no_of_digits=4):
        digits = "0123456789"
        code = ""

        for digit in range(no_of_digits):
            code += digits[floor(random() * 10)]
        return code

    def _is_available(self, otp_code):
        hashed_otp_code = make_password(otp_code)
        # make sure this no currently not used and generated before
        otp = Otp.objects.filter(user=self.user,
                                 code=hashed_otp_code,
                                 otp_type=self.otp_type,
                                 is_verified=False,
                                 valid_until__gte=datetime.utcnow()).first()
        if otp is not None:
            return None
        return hashed_otp_code

    def generate(self, valid_until=5):
        is_not_generated = False
        while is_not_generated is False:
            otp_code = self._generate_code()
            hashed_otp_code = self._is_available(otp_code)
            if hashed_otp_code is not None:
                break

        self.code = hashed_otp_code
        self.valid_until = datetime.utcnow() +\
            timedelta(minutes=valid_until)
        self.save()
        return otp_code

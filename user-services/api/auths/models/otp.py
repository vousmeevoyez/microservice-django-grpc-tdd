"""
    OTP Models
    __________________
"""
from math import floor
from random import random
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db.models import CASCADE, BooleanField, CharField, DateTimeField, ForeignKey
from api.utils.reusable import BaseModel
from api.auths.choices import OTP_TYPES

User = get_user_model()


class Otp(BaseModel):
    """
        Represent OTP Record
    """

    user = ForeignKey(User, on_delete=CASCADE, related_name="otps")
    otp_type = CharField(choices=OTP_TYPES, max_length=100)
    code = CharField(max_length=255)
    valid_until = DateTimeField()
    is_verified = BooleanField(default=False)

    def _generate_code(self, no_of_digits=4):
        """
            Generate Random OTP code
            _____________
            params:
                no_of_digits: int (optional)
        """
        digits = "0123456789"
        code = ""

        for digit in range(no_of_digits):
            code += digits[floor(random() * 10)]
        return code

    def _is_available(self, hashed_otp_code):
        """
            Check does this OTP Code already is available and currently not
            been used before
            ________________________
            params:
                otp_code : str
        """
        # make sure this no currently not used and generated before
        is_available = True
        otp = Otp.objects.filter(
            user=self.user,
            code=hashed_otp_code,
            otp_type=self.otp_type,
            is_verified=False,
            valid_until__gte=datetime.utcnow(),
        ).first()
        if otp is not None:
            is_available = False

        return is_available

    def generate(self, valid_until=5):
        """
            Generate OTP code and make sure the otp code geenrated is available
            ________________________
            params:
                valid_until : int
                    how long otp code should be valid
        """
        is_not_generated = False
        while is_not_generated is not True:
            otp_code = self._generate_code()
            hashed_otp_code = make_password(otp_code)

            if self._is_available:
                break
            # end if
        # end whil
        self.code = hashed_otp_code
        self.valid_until = datetime.utcnow() + timedelta(minutes=valid_until)
        self.save()
        return otp_code

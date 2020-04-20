"""
    OTP Services
"""
from datetime import datetime

from django.contrib.auth.hashers import make_password, check_password

from api.users.models import Otp

from api.users.tasks import send_otp
from api.users.exceptions import (OtpNotFoundException, PendingOtpException,
                                  InvalidOtpException)


class OtpService:

    def __init__(self, user, otp_type="REGISTER"):
        self.user = user
        self.otp_type = otp_type

    def generate_and_send(self):
        """ create otp and entry and send it via celery task"""
        otp = Otp(user=self.user, otp_type=self.otp_type)
        otp_code = otp.generate()
        send_otp.delay(phone_ext=otp.user.phone_ext,
                       phone_no=otp.user.phone_no,
                       otp_code=otp_code)
        return otp.id

    def resend(self):
        """ function to resend otp the only differences we add time validation as
        long there's pending one we prevent it"""
        otp = Otp.objects.filter(user=self.user,
                                 is_verified=False,
                                 valid_until__gte=datetime.utcnow()).first()

        if otp is not None:
            raise PendingOtpException

        # generate new one and send it
        otp_id = self.generate_and_send()
        return otp_id

    @staticmethod
    def verify(otp_id, otp_code):
        """ create otp and entry and send it via celery task"""
        otp = Otp.objects.filter(id=otp_id,
                                 is_verified=False,
                                 valid_until__gte=datetime.utcnow()).first()
        if otp is None:
            raise OtpNotFoundException

        # check otp validity
        if not check_password(otp_code, otp.code):
            raise InvalidOtpException

        otp.is_verified = True
        otp.save()
        return otp

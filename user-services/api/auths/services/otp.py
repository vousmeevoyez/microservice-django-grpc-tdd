"""
    OTP Services
"""
from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

from api.auths.models import Otp

from api.auths.tasks import send_otp
from api.auths.exceptions import (OtpNotFoundException, PendingOtpException,
                                  InvalidOtpException)
from api.users.exceptions import (UserNotFoundException)

User = get_user_model()


class OtpService:

    def __init__(self, user=None, user_id=None, otp_type="REGISTER"):
        self.user = user
        # if user_id is passed we convert it into user
        if user_id is not None:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise UserNotFoundException
            self.user = user
        # end if
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

    def verify(self, otp_id, otp_code):
        """ create otp and entry and send it via celery task"""
        otp = Otp.objects.filter(id=otp_id,
                                 is_verified=False,
                                 valid_until__gte=datetime.utcnow()).first()
        if otp is None:
            raise OtpNotFoundException

        # check otp validity
        if not check_password(otp_code, otp.code):
            raise InvalidOtpException

        # if otp requested is for registration and then otp verified is not
        # same raised and error
        if otp.otp_type != str(self.otp_type):
            raise InvalidOtpException

        otp.is_verified = True
        otp.save()
        return otp

"""
    User Services
"""
from django.contrib.auth import get_user_model
from django.db import DatabaseError, transaction

from api.users.models import (Device, Shop)
from api.users.services import OtpService

from api.users.exceptions import (FailedRegistrationException,
                                  UserNotFoundException)

User = get_user_model()


def create_user(username, password, email, phone_ext, phone_no, first_name,
                middle_name, last_name, shop_name, platform, device_id):
    """ create user + shop + device is still pending until otp is received """

    with transaction.atomic():
        try:
            user = User.objects.create(username=username,
                                       email=email,
                                       phone_ext=phone_ext,
                                       phone_no=phone_no,
                                       first_name=first_name,
                                       middle_name=middle_name,
                                       last_name=last_name)
            user.set_password(password)
            Device.objects.create(platform=platform,
                                  device_id=device_id,
                                  user=user)
            Shop.objects.create(name=shop_name, user=user)
        except DatabaseError as error:
            raise FailedRegistrationException(error)
        else:
            otp_id = OtpService(user).generate_and_send()
    return user, otp_id


def verify_user(otp_id, otp_code):
    """ activate user if user enter valid otp """
    # verify otp
    otp = OtpService.verify(otp_id, otp_code)
    # if valid we activate the user
    user = User.objects.get(id=otp.user.id)
    user.is_active = True
    user.save()


def resend_user_otp(user_id):
    """ resend user otp """
    # verify otp
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise UserNotFoundException
    else:
        otp_id = OtpService(user).resend()
    return otp_id

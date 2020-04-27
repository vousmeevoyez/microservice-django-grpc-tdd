"""
    User Services
"""
from django.contrib.auth import get_user_model
from django.db import DatabaseError, transaction

from api.users.models import (Device)
from api.auths.services import OtpService, update_password
from api.auths.tasks import create_kong_consumer

from api.users.exceptions import (FailedRegistrationException,
                                  OldMsisdnException)

User = get_user_model()


def create_user(password, phone_ext, phone_no, platform, device_id):
    """ create user + shop + device is still pending until otp is received """

    with transaction.atomic():
        try:
            user = User.objects.create(
                phone_ext=phone_ext,
                phone_no=phone_no,
            )
            user.set_password(password)
            user.save()
            Device.objects.create(platform=platform,
                                  device_id=device_id,
                                  user=user)
            otp_id = OtpService(user=user).generate_and_send()
        except DatabaseError as error:
            raise FailedRegistrationException(error)
    return user, otp_id


def verify_user(otp_id, otp_code):
    """ activate user if user enter valid otp """
    # verify otp
    otp = OtpService().verify(otp_id, otp_code)
    # if valid we activate the user
    user_id = otp.user.id
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.save()
    # after that we trigger generate kong consumer
    create_kong_consumer.delay(user_id)


def update_phone_no(user, phone_ext, phone_no):
    """ set new phone_no for user """
    if user.phone_no == phone_no:
        raise OldMsisdnException

    user.phone_ext = phone_ext
    user.phone_no = phone_no
    user.username = phone_ext + phone_no
    user.save()


def update_user_password(user, new_password):
    """ wrap auth services reset passwor here """
    update_password(user, new_password)

"""
    Helper Function
    ____________________
"""
from datetime import datetime, timedelta
from firebase_admin import messaging
import telebot

from rpc.config import ENVIRONMENT, TELEGRAM
from rpc.lib.email import execute, EmailError
from rpc.lib.template import (generate_email_template,
                              generate_notification_template,
                              generate_sms_template)
from rpc.lib.exceptions import BaseError


class HelperError(BaseError):
    """ raised when something wrong with helper """


def send_email(recipient,
               product_type,
               email_type,
               content=None,
               filename=None):
    """ send email based on email category """
    html_template = generate_email_template(product_type, email_type, content)
    try:
        result = execute(recipient, product_type, email_type, html_template,
                         filename)
    except EmailError as error:
        raise HelperError(error.message, error.original_exception)
    return result.status_code


def send_push_notification(device_token,
                           notif_type,
                           product_type,
                           content=None):
    # generate mobile template
    subject, message = generate_notification_template(
        notif_type=notif_type,
        product_type=product_type,
        encoded_content=content)

    # message
    msg = messaging.Message(
        data={
            "title": subject,
            "message": message
        },
        token=device_token,
        # apns=messaging.APNSConfig(payload=payload)
    )
    # send
    res = messaging.send(msg)
    return res


def send_otp(phone_ext, phone_no, content=None):
    if ENVIRONMENT == "DEV":
        # prepare message
        message = generate_sms_template("OTP", content)
        print(message)
        bot = telebot.TeleBot(TELEGRAM["TOKEN"])
        try:
            bot.send_message(TELEGRAM["CHAT_ID"], message)
        except telebot.apihelper.ApiException as error:
            raise HelperError(error)
    return True

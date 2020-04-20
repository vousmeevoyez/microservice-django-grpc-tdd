"""
    User Task
"""
from django.conf import settings
from django.contrib.auth import get_user_model
import grpc

from config import celery_app

from api.utils.utility import encode_content
from api.utils.external import build_kong_client
from api.utils.rpc import otp_pb2, otp_pb2_grpc
from api.utils.exceptions import RemoteCallException


@celery_app.task()
def send_otp(phone_no, phone_ext, otp_code):
    """ send otp via celery so it can safely retried """
    request = otp_pb2.SendSMSOtpRequest()
    request.phone_ext = phone_ext
    request.phone_no = phone_no
    request.content = encode_content({"otp": otp_code})

    try:
        channel = grpc.insecure_channel(
            settings.EXTERNALS["NOTIFICATION"]["BASE_URL"])
        stub = otp_pb2_grpc.OTPServicesStub(channel)
        result = stub.SendSMSOtp(request)
    except grpc.RpcError:
        send_otp.retry()
    return result.status


@celery_app.task()
def create_kong_consumer(user_id):
    """ create kong consumer so later they can use JWT """
    try:
        kong_client = build_kong_client()
        response = kong_client.create_consumer(user_id)
    except RemoteCallException:
        create_kong_consumer.retry()
    else:
        # get user object
        # and store their consumer id there
        user_model = get_user_model()
        user = user_model.objects.get(id=user_id)
        user.consumer_id = response["id"]
        user.save()

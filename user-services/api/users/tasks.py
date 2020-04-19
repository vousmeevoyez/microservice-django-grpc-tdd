"""
    User Task
"""
from django.conf import settings
import grpc

from config import celery_app

from api.utils.utility import encode_content
from api.utils.rpc import otp_pb2, otp_pb2_grpc


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

import pytest
import grpc

from autogen import (
    email_pb2,
    email_pb2_grpc,
    mobile_pb2,
    mobile_pb2_grpc,
    otp_pb2,
    otp_pb2_grpc
)

from google.protobuf.json_format import Parse
'''
def test_send_email(setup_local_client, encode_data):
    stub = email_pb2_grpc.EmailNotificationStub(setup_local_client)
    request = email_pb2.SendEmailRequest()

    request.recipient = "kelvin@modana.id"
    request.product_type = "MOPINJAM"
    request.email_type = "INVESTOR_APPROVE"

    result = stub.SendEmail(request)
    assert result.status == "OK"


def test_send_email_with_content(setup_local_client, encode_data):
    stub = email_pb2_grpc.EmailNotificationStub(setup_local_client)
    request = email_pb2.SendEmailRequest()

    encoded_data = encode_data({"loan_request_code": "12312312312"})
    request.recipient = "kelvin@modana.id"
    request.product_type = "MOPINJAM"
    request.email_type = "LOAN_REQUEST_DISBURSE"
    request.content = encoded_data

    result = stub.SendEmail(request)
    assert result.status == "OK"


def test_send_mobile(setup_local_client, encode_data):
    stub = mobile_pb2_grpc.MobileNotificationStub(setup_local_client)
    request = mobile_pb2.SendPushNotificationRequest()

    request.device_token = "fDrKNYt0JTU:APA91bEtTgIBR1jTgK0ZBeYujPe50uCOHS0V0oFxxG6Fbf3yoN4wgto08pDax8JrPUg05XJf4jexlimue-zBgfZl62_pUpPtxB4QOq63nONPisc4XO2NRyieAXOKk_8foHpUYhW2FAay"
    request.product_type = "MOPINJAM"
    request.notif_type = "LOAN_REQUEST_DISBURSE"
    encoded_data = encode_data({"loan_request_code": "12312312312"})
    request.content = encoded_data

    result = stub.SendPushNotification(request)
    assert result.status == "OK"
'''

def test_send_otp(setup_local_client, encode_data):
    stub = otp_pb2_grpc.OTPServicesStub(setup_local_client)
    request = otp_pb2.SendSMSOtpRequest()

    request.phone_ext = "62"
    request.phone_no = "81219644314"
    encoded_data = encode_data({"otp": "123456"})
    request.content = encoded_data

    result = stub.SendSMSOtp(request)
    assert result.status == "OK"

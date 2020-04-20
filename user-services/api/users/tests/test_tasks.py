"""
    Test Tasks
"""
from unittest.mock import Mock, patch
import pytest
from grpc import RpcError
from celery.exceptions import Retry
from django.contrib.auth import get_user_model

from api.users.tasks import send_otp, create_kong_consumer


@pytest.mark.django_db
@patch("api.utils.rpc.otp_pb2_grpc.OTPServicesStub")
def test_send_otp_success(mock_rpc):
    """ mock celery task succeed when sending otp """
    mock_rpc.return_value.SendSMSOtp.return_value = Mock(status="OK")
    result = send_otp("62", "81219644314", "123456")
    assert result == "OK"


@pytest.mark.django_db
@patch("api.utils.rpc.otp_pb2_grpc.OTPServicesStub")
def test_send_otp_failed(mock_rpc):
    """ mock celery task failed when sending otp """
    mock_rpc.return_value.SendSMSOtp.side_effect = RpcError

    with pytest.raises(Retry):
        send_otp("62", "81219644314", "123456")


@pytest.mark.django_db
@patch("requests.request")
def test_create_kong_consumer(mock_request, create_consumer_response, user):
    """ mock celery task failed when sending otp """
    mock_request.return_value.status_code.return_value = 201
    mock_request.return_value.json.return_value =\
        create_consumer_response

    create_kong_consumer(str(user.id))
    # make sure user has consumer id now
    user_model = get_user_model()
    user = user_model.objects.get(id=user.id)
    assert str(user.consumer_id) == create_consumer_response["id"]

from unittest.mock import Mock, patch
import pytest
from grpc import RpcError
from celery.exceptions import Retry

from api.users.tasks import send_otp


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

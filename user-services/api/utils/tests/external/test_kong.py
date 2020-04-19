
from unittest.mock import Mock, patch
from api.utils.external.kong import KongAPI


def test_create_consumer(create_consumer_response):
    mock_remote_call = Mock()
    mock_remote_call.execute.return_value = 201, create_consumer_response

    response = KongAPI(mock_remote_call).create_consumer("some-user-id")
    assert response == create_consumer_response

def test_create_jwt_credential(create_jwt_credential_response):
    mock_remote_call = Mock()
    mock_remote_call.execute.return_value = 201, create_jwt_credential_response

    response = KongAPI(mock_remote_call).create_jwt_credential("some-consumer-id")
    assert response == create_jwt_credential_response

def test_delete_jwt_credential():
    mock_remote_call = Mock()
    mock_remote_call.execute.return_value = 204, None

    status_code = KongAPI(mock_remote_call).delete_jwt_credential("some-consumer-id")
    assert status_code == 204

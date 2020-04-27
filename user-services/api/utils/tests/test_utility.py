import pytest

from requests.exceptions import HTTPError

from unittest.mock import patch
from api.utils.utility import RemoteCall
from api.utils.exceptions import RemoteCallException


@patch("requests.request")
def test_remote_calL_success(mock_request):
    mock_request.return_value.status_code = 200
    mock_request.return_value.json.return_value = {"something": "returned"}

    status_code, response = RemoteCall().execute(
        "POST", "http://some-url", {"hello": "world!"}
    )
    assert status_code == 200
    assert response["something"] == "returned"


@patch("requests.request")
def test_remote_call_failed(mock_request):
    mock_request.side_effect = HTTPError

    with pytest.raises(RemoteCallException):
        RemoteCall().execute("POST", "http://some-url", {"hello": "world!"})

import json
import base64

import grpc
import pytest


@pytest.fixture
def setup_local_client():
    """ fixture to connect grpc client to grpc server """
    return grpc.insecure_channel("127.0.0.1:5001")
    #return grpc.insecure_channel("127.0.0.1:11003")


@pytest.fixture
def encode_data():
    def _encode_data(data):
        json_string = json.dumps(data)
        encoded_json_string = json_string.encode("utf-8")
        base64_string = base64.b64encode(encoded_json_string).decode("utf-8")
        return base64_string

    return _encode_data

"""
    Utility
"""
import json
import base64

import requests
import logging

from api.utils.exceptions import RemoteCallException

LOGGER = logging.getLogger(__name__)


def encode_content(payload):
    encoded_payload = json.dumps(payload).encode("utf-8")
    data = base64.b64encode(encoded_payload).decode("utf-8")
    return data


class RemoteCall:
    def __init__(self):
        pass

    def execute(method, url, data=None, headers=None):
        try:
            LOGGER.info("URL: %s", url)
            LOGGER.info("DATA: %s", data)
            r = requests.request(method=method, url=url, json=data, headers=headers)
            LOGGER.info("STATUS CODE: %s", r.status_code)
            LOGGER.info("RESPONSE: %s", r.text)
            r.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise RemoteCallException(str(error))
        except requests.exceptions.ConnectionError as error:
            raise RemoteCallException(str(error))
        else:
            if r.status_code == 204:
                return r.status_code, None
            return r.status_code, r.json()

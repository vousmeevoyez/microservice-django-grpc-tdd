"""
    Kong helper function
"""
from django.conf import settings

PREFIX = "admin-api"
ENDPOINTS = {
    "CONSUMERS": PREFIX + "/consumers/",
    "JWT": PREFIX + "/consumers/{}/jwt",
    "JWT_DETAIL": PREFIX + "/consumers/{}/jwt/{}",
}
BASE_URL = settings.EXTERNALS["KONG"]["BASE_URL"]


class KongAPI:
    def __init__(self, remote_call):
        self._remote_call = remote_call
        self._headers = {"apikey": settings.EXTERNALS["KONG"]["API_KEY"]}

    def _execute(self, method, url, payload=None):
        status_code, response = self._remote_call.execute(
            method, url, payload, self._headers
        )
        return status_code, response

    def create_consumer(self, user_id):
        """ create kong consumer """
        url = BASE_URL + ENDPOINTS["CONSUMERS"]
        payload = {"custom_id": user_id}
        status_code, response = self._execute("POST", url, payload)
        return response

    def create_jwt_credential(self, consumer_id):
        """ create jwt for consumer """
        url = BASE_URL + ENDPOINTS["JWT"].format(consumer_id)
        status_code, response = self._execute("POST", url)
        return response

    def delete_jwt_credential(self, consumer_id, jwt_id):
        """ delete jwt for consumer """
        url = BASE_URL + ENDPOINTS["JWT_DETAIL"].format(consumer_id, jwt_id)
        status_code, response = self._execute("DELETE", url)
        return status_code

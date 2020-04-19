"""
    User Services
"""
import jwt
from django.contrib.auth import get_user_model, authenticate
from django.db import DatabaseError, transaction

from api.utils.external import build_kong_client
from api.users.exceptions import (FailedRegistrationException,
                                  InvalidCredentialsException,
                                  InactiveUserException)

User = get_user_model()
CLIENT = build_kong_client()


class JWTToken:

    def __init__(self, user_id):
        self.user_id = user_id
        self.user = User.objects.get(id=user_id)

    def generate(self):
        """ Generate actual jwt token here """
        response = CLIENT.create_jwt_credential(self.user.consumer_id)
        # current set expiration to 0
        current_exp = 0  # means infnite
        algorithm = "HS256"
        # accepted jwt payload by kong
        payload = {
            "exp": current_exp,
            "iss": response["key"],
            "iat": response["created_at"],
            "sub": str(self.user.id),
        }
        return jwt.encode(payload, response["key"], algorithm)

    def remove(self):
        """ Remove jwt token here """
        CLIENT.delete_jwt_credential(self.user.consumer_id)


def login(username, password):
    auth_user = authenticate(username=username, password=password)
    if auth_user is not None:
        # generate jwt here
        token = JWTToken(auth_user.id).generate()
        return {"access_token": token.decode("utf-8")}
    else:
        # event if its none we make sure does this user really exist or not
        # because by default django return none for inactive user
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise InvalidCredentialsException
        else:
            if user is not None and user.is_active is False:
                raise InactiveUserException


def logout(user_id):
    return JWTToken(user_id).remove()

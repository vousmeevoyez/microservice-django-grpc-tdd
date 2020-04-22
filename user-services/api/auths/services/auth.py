"""
    Auth Services
"""
import jwt
from django.contrib.auth import get_user_model, authenticate

from api.auths.services.otp import OtpService
from api.utils.external import build_kong_client
from api.auths.exceptions import (InvalidCredentialsException,
                                  InactiveUserException)

User = get_user_model()
CLIENT = build_kong_client()


class JWTToken:
    """ Create JWT Model to abstract checking and generating JWT """

    def __init__(self, user_id):
        """ convert user_id into actual user object """
        self.user = User.objects.get(id=user_id)

    def generate(self):
        """ Generate actual jwt token """
        response = CLIENT.create_jwt_credential(self.user.consumer_id)
        # current set expiration to 0
        current_exp = 0  # means infnite
        current_nbf = 0  # means infnite
        algorithm = "HS256"
        # accepted jwt payload by kong
        payload = {
            "exp": current_exp,
            "nbf": current_nbf,
            "iss": response["key"],
            "iat": response["created_at"],
            "sub": str(self.user.id),
        }
        return jwt.encode(payload, response["secret"], algorithm)

    def remove(self):
        """
            blacklist issued jwt token
            this will also trigger remove generated credentials on API Gateway
            ________________________
        """
        CLIENT.delete_jwt_credential(self.user.consumer_id)


def login(username, password):
    """
        check username and password, if valid we issue a JWT otherwise we raise
        Exception
        _________________________
        params:
            username: str
            password: str

        exception:
            InvalidCredentialsException
            InactiveUserException

        return:
            dict containing access_token
    """
    auth_user = authenticate(username=username, password=password)
    if auth_user is None:
        # if its none we make sure does this user really exist or not
        # because by default django return none for inactive user
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise InvalidCredentialsException
        else:
            if user is not None and user.is_active is False:
                raise InactiveUserException

    token = JWTToken(auth_user.id).generate()
    return {"access_token": token.decode("utf-8")}


def logout(user_id):
    """
        black list issued jwt token
        _________________________
        params:
            user_id: str
    """
    JWTToken(user_id).remove()


def request_reset_password(user_id):
    """
        send otp to notify they really reset their password
        __________________________
        params:
            user_id: str
    """
    otp_id = OtpService(user_id=user_id,
                        otp_type="RESET_PASSWORD").generate_and_send()
    return {"otp_id": otp_id}


def reset_password(otp_id, otp_code, password, **ignore):
    """
        reset password and verifying otp code that sent before
        __________________________
        params:
            otp_id: str
            otp_code: str
            password: str
    """
    # verify is it correct otp or not
    otp = OtpService(otp_type="RESET_PASSWORD").verify(otp_id, otp_code)
    # set new password for user
    user = otp.user
    user.set_password(password)
    user.save()

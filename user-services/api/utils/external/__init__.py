"""
    Package init
"""
from api.utils.utility import RemoteCall
from api.utils.external.kong import KongAPI


def build_kong_client():
    """ initialize kong client """
    return KongAPI(RemoteCall)

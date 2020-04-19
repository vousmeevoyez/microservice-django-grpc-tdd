"""
    gRPC Server
    ___________________
    this is where we register servicer class and start gRPC Server
"""
import time
import grpc
from concurrent import futures

from firebase_admin import credentials, initialize_app

from autogen import (email_pb2_grpc, mobile_pb2_grpc, otp_pb2_grpc)

from rpc.services import (EmailServices, MobileServices, OTPServices)

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def start(host, port):
    """ start Async gRPC Server"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # register GRPC Servicer here
    email_pb2_grpc.add_EmailServicesServicer_to_server(EmailServices(), server)
    mobile_pb2_grpc.add_MobileServicesServicer_to_server(
        MobileServices(), server)
    otp_pb2_grpc.add_OTPServicesServicer_to_server(OTPServices(), server)
    # start
    # init firebase
    #cred = credentials.Certificate("secret.json")
    #initialize_app(cred)

    server.add_insecure_port("{}:{}".format(host, port))
    server.start()
    print("Listening gRPC server at {}:{}".format(host, port))
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    start()

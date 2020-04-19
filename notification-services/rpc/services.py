import grpc

from autogen import (email_pb2_grpc, email_pb2, mobile_pb2_grpc, mobile_pb2,
                     otp_pb2_grpc, otp_pb2)

from google.protobuf.json_format import MessageToDict
from google.protobuf.json_format import Parse

from rpc.lib.helper import (send_email, send_push_notification, send_otp,
                            HelperError)


class EmailServices(email_pb2_grpc.EmailServicesServicer):
    def SendEmail(self, request, context):
        """ handle RPC For sending email """
        payload = MessageToDict(request, preserving_proto_field_name=True)
        response = email_pb2.SendEmailResponse()
        try:
            result = send_email(**payload)
        except HelperError as error:
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
            context.set_details(error.message)
        else:
            if result == 202:
                response.status = "OK"
        return response


class MobileServices(mobile_pb2_grpc.MobileServicesServicer):
    def SendPushServices(self, request, context):
        """ handle RPC For sending push notification to mobile  """
        payload = MessageToDict(request, preserving_proto_field_name=True)
        response = mobile_pb2.SendPushServicesResponse()
        try:
            send_push_notification(**payload)
        except HelperError as error:
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
            context.set_details(error.message)
        else:
            response.status = "OK"
        return response


class OTPServices(otp_pb2_grpc.OTPServicesServicer):
    def SendSMSOtp(self, request, context):
        """ handle RPC For sending otp """
        payload = MessageToDict(request, preserving_proto_field_name=True)
        response = otp_pb2.SendSMSOtpResponse()
        try:
            send_otp(**payload)
        except HelperError as error:
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
            context.set_details(error.message)
        else:
            response.status = "OK"
        return response

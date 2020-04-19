"""
    Testing Template Engine
"""
from rpc.lib.template import (TemplateEngine, decode_content,
                              generate_sms_template)


def test_decode_content(encode_data):
    raw = {"message": "Hello World!"}
    result = decode_content(encode_data(raw))
    assert result == raw


def test_generate_sms_template(encode_data):
    raw = {"otp": "123456"}
    encoded_content = encode_data(raw)
    result = generate_sms_template("OTP", encoded_content)
    print(result)

from rpc.lib.helper import send_email, send_otp
'''
def test_send_email(encode_data):
    recipient = "kelvin@modana.id"
    product_type = "MOPINJAM"
    email_type = "INVESTOR_APPROVE"
    # fake_content = encode_data(fake_content)
    status_code = send_email(recipient, product_type, email_type)
    assert status_code == 202
'''


def test_send_otp(encode_data):
    phone_ext = "62"
    phone_no = "81219644314"
    encoded_content = encode_data({"otp": "123456"})
    # fake_content = encode_data(fake_content)
    result = send_otp(phone_ext=phone_ext,
                      phone_no=phone_no,
                      content=encoded_content)
    assert result

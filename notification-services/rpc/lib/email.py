"""
    Email Module
    _______________
    responsible to sending email via sengrid
"""
import os
import base64

# send grid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail,
    Attachment,
    FileContent,
    FileName,
    FileType,
    Disposition,
    ContentId,
)
from sendgrid.helpers.mail.attachment import Attachment
from sendgrid.helpers.mail.content import Content

from rpc.lib.exceptions import BaseError
from rpc.const import EMAIL_STATIC, EMAIL_TEMPLATES

API_KEY = os.environ.get("EMAIL_API_KEY")


class EmailError(BaseError):
    """ raised when something went wrong while sending email """


def create_attachment(filename):
    """ create sendgrid attachment """
    with open(filename, "rb") as f:
        data = f.read()

    # split filename only
    folder, filename = filename.split("/")

    encoded = base64.b64encode(data).decode()
    attachment = Attachment()
    attachment.file_content = FileContent(encoded)
    attachment.file_type = FileType(
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    attachment.file_name = FileName(filename)
    attachment.disposition = Disposition("attachment")
    attachment.content_id = ContentId("Example Content ID")
    return attachment


def prepare_email(sender, to, subject, html_template, attachment=None):
    """ prepare sendgrid email """
    message = Mail(
        from_email=sender, to_emails=to, subject=subject, html_content=html_template
    )

    if attachment is not None:
        message.attachment = attachment

    sg = SendGridAPIClient(API_KEY)
    return sg, message


def execute(recipients, product_type, email_type, html_template, filename=None):
    """ send email through sendgrid """
    # convert filename to attachment
    attachment = None
    if filename is not None:
        attachment = create_attachment(filename)

    # based on product get right subject and sender!
    sender = EMAIL_STATIC[product_type]["FROM"]
    subject = EMAIL_TEMPLATES[product_type]["SUBJECT"][email_type]

    sg, mail = prepare_email(sender, recipients, subject, html_template, attachment)

    try:
        response = sg.send(mail)
    except Exception as e:
        raise EmailError("SENDING_FAILED", e)
    else:
        print(response.status_code)
    return response

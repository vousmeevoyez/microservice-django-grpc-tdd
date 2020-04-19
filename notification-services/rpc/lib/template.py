"""
    Template Render
    ________________
    module responsible to generating correct email html template!
"""
from string import Template
import json
import base64

from jinja2 import Environment, FileSystemLoader
from rpc.const import (EMAIL_STATIC, EMAIL_TEMPLATES, MOBILE_TEMPLATES,
                       SMS_TEMPLATES)


class TemplateEngine:
    """ template engine"""
    def __init__(self, template_name, data, templatedir="rpc/templates"):
        self.env = Environment(loader=FileSystemLoader(templatedir))
        self.template_name = template_name
        self.data = data

    def render(self):
        """ fetch selected template replace the placeholder and render it to
        string """
        template = self.env.get_template(self.template_name + ".html")
        template = template.render(self.data)
        return template


def decode_content(encoded_content):
    encoded_content = encoded_content.encode("utf-8")
    return json.loads(base64.b64decode(encoded_content).decode("utf-8"))


def merge_content(content1, content2):
    content = {**content1, **content2}
    return content


def parse_to_template(string_template, data):
    """ convert string into template and replace the placeholder with actual
    data """
    template = Template(string_template)
    parsed_template = template.substitute(data)
    return parsed_template


def generate_email_template(product_type, email_type, encoded_content=None):
    """ based on category we generate the right email html along with its
    content"""
    # fetch static info like street, etc
    email_static = EMAIL_STATIC[product_type]
    # fetch content based on email type
    email_content = {
        "CONTENT": EMAIL_TEMPLATES[product_type]["CONTENT"][email_type]
    }

    decoded_content = None
    if encoded_content is not None:
        # decode encoded data
        decoded_content = decode_content(encoded_content)
        parsed_template = parse_to_template(
            string_template=email_content["CONTENT"], data=decoded_content)
        email_content["CONTENT"] = parsed_template
    # add it with the static!
    data = merge_content(email_static, email_content)

    email_template = TemplateEngine(
        template_name=EMAIL_TEMPLATES[product_type]["TEMPLATE"][email_type],
        data=data).render()
    return email_template


def generate_notification_template(product_type,
                                   notif_type,
                                   encoded_content=None):
    """ based on notification mobile """
    # fetch static info like street, etc
    # fetch content based on email type
    subject = MOBILE_TEMPLATES[product_type]["SUBJECT"][notif_type]
    message = MOBILE_TEMPLATES[product_type]["CONTENT"][notif_type]
    if encoded_content is not None:
        decoded_content = decode_content(encoded_content)
        parsed_template = parse_to_template(string_template=message,
                                            data=decoded_content)
        message = parsed_template

    return subject, message


def generate_sms_template(sms_type, encoded_content):
    """ based on notification mobile """
    # fetch static info like street, etc
    # fetch content based on email type
    message = SMS_TEMPLATES[sms_type]
    decoded_content = decode_content(encoded_content)
    parsed_template = parse_to_template(string_template=message,
                                        data=decoded_content)
    message = parsed_template
    return message

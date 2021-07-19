import smtplib
from email.mime.text import MIMEText

import jwt

from uer_register_login.models import CustomUser
from user_auth import settings
from rest_framework.response import Response


def send_email(token):
    server = smtplib.SMTP_SSL(settings.SMTP_SSL, 465)
    server.login(settings.USR_NAME, settings.USR_PASSWORD)
    msg = MIMEText(f'<a href="http://127.0.0.1:8000/url/verify/{token}">abc</a>', 'html')
    server.sendmail(settings.FROM, settings.TO, msg.as_string())
    server.quit()


def token_decoder(function):
    def wrapper(self, request):
        if 'HTTP_AUTHORIZATION' not in request.META:
            resp = Response({'message': 'Token not provided in the header'})
            resp.status_code = 400
            return resp
        key = "secret"
        usr_details = jwt.decode(request.META.get('HTTP_AUTHORIZATION'), key=key, algorithms="HS256")
        usr_id = usr_details.get("usr_id")
        request.data.update({"id": usr_id})
        return function(self, request)

    return wrapper


def register_encode_token(usr_name):
    key = "secret"
    token = jwt.encode({"username": usr_name}, key, algorithm="HS256")
    return token


def login_encode_token(temp):
    key = "secret"
    token = jwt.encode({"usr_id": CustomUser.objects.get(username=temp.get("username")).id}, key, algorithm="HS256")
    return token

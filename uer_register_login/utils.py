import smtplib
from datetime import timedelta
from email.mime.text import MIMEText
from django.http import QueryDict
import jwt
from jwt import ExpiredSignatureError
import logging
from uer_register_login.models import CustomUser
from user_auth import settings
from rest_framework.response import Response
from user_auth.settings import KEY
import redis


def send_email(token, user_email):
    """
    sends email to registered user to verify itself
    :param user_email:
    :param token: the token containing user credentials
    :return: pass
    """
    try:
        server = smtplib.SMTP_SSL(settings.SMTP_SSL, 465)
        server.login(settings.USR_NAME, settings.USR_PASSWORD)
        msg = MIMEText(f'<a href="http://127.0.0.1:8000/user/verify/{token}">abc</a>', 'html')
        server.sendmail(settings.FROM, user_email, msg.as_string())
        server.quit()
    except smtplib.SMTPException as e:
        return e.args


def token_decoder(function):
    """
    outer function that act as base for deco
    :param function: takes function as argument that will be decorated
    :return: decorated function
    """

    def wrapper(self, request):
        """
        function act as inner function
        :param self: pass
        :param request: the http request
        :return: function name
        """
        if 'HTTP_AUTHORIZATION' not in request.META:
            resp = Response({'message': "token not found"})
            resp.status_code = 400
            return resp
        # connection_2 = redis.ConnectionPool(host='localhost', port=6379, db=0)
        # r = redis.Redis(connection_pool=connection_2)
        usr_details = jwt.decode(request.META.get('HTTP_AUTHORIZATION'), key=KEY, algorithms="HS256")
        # if r.exists(usr_details.get("usr_id")) is None:
        #     return Response({"message": "USER IS NOT LOGGED IN , LOGIN AGAIN"}, status=403)
        usr_id = usr_details.get("usr_id")
        if isinstance(request.data, QueryDict):
            request.data._mutable = True
        request.data.update({'user': usr_id})
        return function(self, request)

    return wrapper


def register_encode_token(usr_name):
    try:
        token = jwt.encode({"username": usr_name}, KEY, algorithm="HS256")
        return token
    except ExpiredSignatureError as e:
        return Response({"message": "Token Not Found or expired"}, status=404)
    except Exception as e:
        return "something went wrong"


def login_encode_token(temp):
    try:
        token = jwt.encode({"usr_id": CustomUser.objects.get(username=temp.get("username")).id,
                            "usr_name": CustomUser.objects.get(username=temp.get("username")).username,
                            }
                           , KEY, algorithm="HS256")
        return token
    except ExpiredSignatureError as e:
        return Response({"message": "Token Not Found or expired"}, status=404)
    except Exception:
        return "something went wrong"


def returns_user_logger():
    """
    this method is used to create and configure logger
    :return: returns configured logger
    """
    log_file_format = '%(asctime)s %(message)s {%(pathname)s:%(lineno)d}'
    user_logger = logging.getLogger(__name__)
    user_log_handler = logging.FileHandler('user_error_files.log', mode='w')
    user_log_handler.setLevel(logging.DEBUG)
    user_log_handler.setFormatter(logging.Formatter(log_file_format))
    user_logger.addHandler(user_log_handler)
    return user_logger


user_log = returns_user_logger()

from datetime import timedelta

from drf_yasg.utils import swagger_auto_schema
from uer_register_login.utils import user_log
from .models import CustomUser
from rest_framework.views import APIView
from rest_framework.response import Response
from .serialize import RegisterUserSer, LoginUserSerializer
from django.core.exceptions import ValidationError, ObjectDoesNotExist
import jwt
from jwt.exceptions import ExpiredSignatureError
from . import utils
import redis
from redis.exceptions import ConnectionError
from drf_yasg import openapi


class LoginView(APIView):
    # class representing view for user registration

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description="username of user"),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description="password of user"),
        }))
    def post(self, request):
        """
        this method login user to system
        :param request: http request to made to this api
        :return: it returns response to request that is made:
        """
        try:
            if (not request.data.get("username")) or (not request.data.get("password")):
                user_log.error("invalid input ")
                return Response({"message": "invalid input"})
            deserialized_data = LoginUserSerializer(data=request.data)
            deserialized_data.is_valid()
            temp = deserialized_data.data
            if CustomUser.objects.filter(username=temp.get("username")).filter(password=temp.get("password")):
                if CustomUser.objects.get(username=temp.get("username")).verified:
                    token = utils.login_encode_token(temp)
                    usr_details = jwt.decode(token, key="secret", algorithms="HS256")
                    connection_1 = redis.ConnectionPool(host='localhost', port=6379, db=0)
                    r = redis.Redis(connection_pool=connection_1)
                    r.setex(usr_details.get("usr_id"), timedelta(days=2), usr_details.get("usr_name"))
                    return Response({"message": "USER LOGGED IN", "data": {"token": token}}, status=200)
                else:
                    return Response({"message": "USER NOT VERIFIED"}, status=400)
            else:
                raise ObjectDoesNotExist
        except ObjectDoesNotExist as e:
            user_log.exception("object not found exception occurred")
            return Response({"message": "USER NOT FOUND"}, status=404)
        except ConnectionError as e:
            user_log.exception("redis connection exception occurred")
            return Response({"message": "Redis Connection Error"}, status=502)
        except ExpiredSignatureError as e:
            user_log.exception("token not found exception occurred")
            return Response({"message": "Token Not Found or expired"}, status=404)
        except Exception as e:
            user_log.exception("generic exception occurred")
            return Response({"message": "something went wrong"}, status=400)


class RegisterView(APIView):
    # class representing view for user login

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description="username of user"),
            'first_name': openapi.Schema(type=openapi.TYPE_STRING, description="first_name of user"),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description="email of user"),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description="password of user"),
        }))
    def post(self, request):
        """
        this method is used to register user or save user in database
        :param request: http request to made to this api
        :return: it returns response to request that is made:
        """
        try:
            if (not request.data.get("username")) or (not request.data.get("first_name")) or (
                    not request.data.get("email")) or (not request.data.get("password")):
                user_log.error("invalid input ")
                return Response({"message": "invalid input"})
            new_usr = CustomUser(username=request.data.get("username"), first_name=request.data.get("first_name"),
                                 email=request.data.get("email"), password=request.data.get("password"))
            print(new_usr)
            serializer = RegisterUserSer(new_usr)
            deserialized_data = RegisterUserSer(data=serializer.data)
            if deserialized_data.is_valid():
                deserialized_data.save()
                token = utils.register_encode_token(request.data.get("username"))
                utils.send_email(token, request.data.get("email"))
                return Response({"message": "VERIFY YOURSELF, CHECK EMAIL"}, status=200)
            return Response({"message": "DATA SERIALIZATION AND VALIDATION FAILED"}, status=400)
        except ValidationError as e:
            user_log.exception("data validation failed")
            return Response({"message": e.message})
        except ExpiredSignatureError as e:
            user_log.exception("token not found exception occurred")
            return Response({"message": "Token Not Found or expired"}, status=404)
        except Exception as e:
            user_log.exception("generic exception occurred")
            return Response({"message": "something went wrong"}, status=400)


class VerifyView(APIView):
    # this class contain method for verification of user

    def get(self, request, token):
        """
        this method does the verification and confirmation if user successfully registered or not
        :param request: the request body
        :param token: token that contains credentials of user
        :return: returns corresponding response to users request
        """
        try:
            encoded = token
            key = "secret"
            usr_details = jwt.decode(encoded, key=key, algorithms="HS256")
            usr_name = usr_details.get("username")
            check = CustomUser.objects.get(username=usr_name)
            if check:
                check.verified = True
                check.save()
                return Response({"message": "VERIFIED"}, status=200)
            return Response({"message": "SOME THING WENT WRONG"}, status=400)
        except Exception as e:
            user_log.exception("generic exception occurred")
            return Response({"message": "SOMETHING WENT WRONG",
                             "detail": e.args}, status=400)

from datetime import timedelta
from .models import CustomUser
from rest_framework.views import APIView
from rest_framework.response import Response
from .serialize import RegisterUserSer, LoginUserSerializer
from django.core.exceptions import ValidationError, ObjectDoesNotExist
import jwt
from . import utils
import redis


class LoginView(APIView):
    # class representing view for user registration

    def post(self, request):
        """
        this method is used to register user or save user in database
        :param request: http request to made to this api
        :return: it returns response to request that is made:
        """
        try:
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
            return Response({"message": "USER NOT FOUND"}, status=404)
        except Exception as e:
            return Response({"message": "something went wrong"}, status=400)


class RegisterView(APIView):
    # class representing view for user login

    def post(self, request):
        """
       this method login user to system
        :param request: http request to made to this api
        :return: it returns response to request that is made:
        """
        try:
            new_usr = CustomUser(username=request.data.get("username"), first_name=request.data.get("first_name"),
                                 email=request.data.get("email"), password=request.data.get("password"))
            serializer = RegisterUserSer(new_usr)
            deserialized_data = RegisterUserSer(data=serializer.data)
            if deserialized_data.is_valid():
                deserialized_data.save()
                token = utils.register_encode_token(request.data.get("username"))
                utils.send_email(token)
                return Response({"message": "VERIFY YOURSELF, CHECK EMAIL"}, status=200)
            return Response({"message": "USERNAME VALIDATION FAILS"}, status=400)
        except ValidationError as e:
            return Response(e.message)


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
            return Response({"message": "SOMETHING WENT WRONG",
                             "detail": e.args}, status=400)

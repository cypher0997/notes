from .models import CustomUser
from rest_framework import serializers
from django.core.exceptions import ValidationError


class RegisterUserSer(serializers.ModelSerializer):
    # it is class which serialize the data
    class Meta:
        model = CustomUser
        fields = "__all__"

    def validate_username(self, value):
        """
        this method validates the deserialized data
        :param value: username that is to be validated
        :return: returns username for further operations
        """
        if CustomUser.objects.filter(username=value):
            raise ValidationError("DUPLICATION OF RECORD")
        else:
            return value


class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"

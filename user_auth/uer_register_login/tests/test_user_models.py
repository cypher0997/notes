from uer_register_login.models import CustomUser
import pytest


@pytest.mark.django_db
class TestModels:
    def test_user_exists(self):
        """
        this method is used to test the models in user register and login api
        :return: true or false
        """
        data = CustomUser.objects.filter(pk=1)
        assert isinstance(data, CustomUser) == True

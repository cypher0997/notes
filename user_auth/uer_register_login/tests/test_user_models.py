from uer_register_login.models import CustomUser
import pytest
from mixer.backend.django import mixer


@pytest.mark.django_db
class TestModels:
    def test_user_exists(self):
        """
        this method is used to test the models in user register and login api
        :return: true or false
        """
        usr_instance = mixer.blend(CustomUser, id=1)
        assert isinstance(usr_instance, CustomUser) == True

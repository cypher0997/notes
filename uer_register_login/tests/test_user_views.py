from uer_register_login.models import CustomUser
import pytest
from django.urls import resolve, reverse
from mixer.backend.django import mixer



class TestViews:
    # this class contains methods to test views of user register and login views
    @pytest.mark.django_db
    def test_register_view(self, client):
        """
        to test register view
        :param client: handles request
        :return: true or false
        """
        url = reverse('uer_register_login:register_method')
        data = {
            "username": "SUMAN",
            "first_name": "suman",
            "email": "suman@gmail.com",
            "password": "55566622"
        }
        res = client.post(url, data)
        assert res.status_code == 200

    @pytest.mark.django_db
    def test_login_view(self, client):
        """
        to test login view
        :param client: handles request
        :return: true or false
        """
        user = CustomUser.objects.create(username='BHASKAR', first_name='bhaskar', email='abc@gmail.com',
                                         password='55566622', verified=True)
        user.save()
        url = reverse('uer_register_login:login_method')
        data = {
            "username": "BHASKAR",
            "password": "55566622"
        }
        res = client.post(url, data)
        assert res.status_code == 200

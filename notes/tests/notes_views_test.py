import pytest
from django.urls import reverse
from uer_register_login.models import CustomUser
from notes.models import NewNotes
from mixer.backend.django import mixer
import json


@pytest.mark.django_db
class TestNotes:
    def test_create_notes(self, client):
        user = CustomUser.objects.create(username='raman', password='55566622', email='raman@gmail.com',
                                         first_name='raman', verified=True)
        user.save()
        url = reverse('uer_register_login:login_method')
        data = {
            "username": "raman",
            "password": "55566622"
        }
        res = client.post(url, data)
        content = json.loads(res.content)
        print(res.content)
        data = {
            'title': 'something',
            'discription': 'again_something'
        }
        header = {"HTTP_AUTHORIZATION": content.get("data").get("token")}
        url = reverse('notes')
        res = client.post(url, data, **header)
        print(res.content)
        assert res.status_code == 200

    def test_retrieve_notes(self, client):
        user = CustomUser.objects.create(username='raman', password='55566622', email='raman@gmail.com',
                                         first_name='raman', verified=True)
        user.save()
        url = reverse('uer_register_login:login_method')
        data = {
            "username": "raman",
            "password": "55566622"
        }
        res = client.post(url, data)
        content = json.loads(res.content)
        header = {"HTTP_AUTHORIZATION": content.get("data").get("token")}
        url = reverse('notes')
        data = {
            'user': 1,
        }
        res = client.post(url, data, **header)
        assert res.status_code == 200

    def test_update_notes(self, client):
        user = CustomUser.objects.create(username='raman', password='55566622', email='raman@gmail.com',
                                         first_name='raman', verified=True)
        user.save()
        url = reverse('uer_register_login:login_method')
        data = {
            "username": "raman",
            "password": "55566622"
        }
        res = client.post(url, data)
        content = json.loads(res.content)
        data = {
            'id': 1,
            'title': 'something new',
            'discription': 'again_something new'
        }
        header = {"HTTP_AUTHORIZATION": content.get("data").get("token")}
        url = reverse('notes')
        res = client.put(url, data, **header, content_type='application/json')
        print(res.content)
        assert res.status_code == 200

    def test_delete_notes(self, client):
        user = CustomUser.objects.create(username='raman', password='55566622', email='raman@gmail.com',
                                         first_name='raman', verified=True)
        user.save()
        url = reverse('uer_register_login:login_method')
        data = {
            "username": "raman",
            "password": "55566622"
        }
        res = client.post(url, data)
        content = json.loads(res.content)
        data = {
            'id': 1
        }
        header = {"HTTP_AUTHORIZATION": content.get("data").get("token")}
        url = reverse('notes')
        res = client.delete(url, data, **header, content_type='application/json')
        print(res.content)
        assert res.status_code == 200
import pytest
from django.urls import reverse
from uer_register_login.models import CustomUser
from notes.models import NewNotes
from mixer.backend.django import mixer


@pytest.mark.django_db
class TestNotes:
    def test_create_notes(self, client):
        url = reverse('notes')
        user = CustomUser.objects.create(username='raman', password='raman123rag', email='raman@gmail.com',
                                         first_name='raman')
        user.save()

        data = {
            'user': 1,
            'title': 'something',
            'discription': 'again_something'
        }
        res = client.post(url, data, content_type='application/json')
        assert res.status_code == 200

    def test_retrieve_notes(self, client):
        url = reverse('notes')
        user = CustomUser.objects.create(username='raman', password='raman123rag', email='raman@gmail.com',
                                         first_name='raman')
        user.save()
        data = {
            'user': 1,
        }
        res = client.post(url, data, content_type='application/json')
        assert res.status_code == 200

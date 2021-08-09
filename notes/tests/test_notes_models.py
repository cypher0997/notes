from mixer.backend.django import mixer
from notes.models import NewNotes
import pytest


@pytest.mark.django_db
class TestModels:
    # class contains methods to test models in notes api
    def test_note_exists(self):
        """
        method to test models in notes api
        :return:true or false
        """
        usr_inst = mixer.blend(NewNotes, id=1)
        assert usr_inst.is_notes_instance == True

    def test_note_not_exists(self):
        """
        methods to test models incorrectly in notes api
        :return: true or false
        """
        usr_inst = mixer.blend(NewNotes, id=0)
        assert usr_inst.is_notes_instance == False

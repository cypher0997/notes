from mixer.backend.django import mixer
from notes.models import Notes, Label
import pytest


@pytest.mark.django_db
class TestModels:
    # class contains methods to test models in notes api
    def test_note_exists(self):
        """
        method to test models in notes api
        :return:true or false
        """
        notes_inst = mixer.blend(Notes, id=1)
        assert notes_inst.is_notes_instance == True

    def test_note_not_exists(self):
        """
        methods to test models incorrectly in notes api
        :return: true or false
        """
        notes_inst = mixer.blend(Notes, id=0)
        assert notes_inst.is_notes_instance == False

    def test_label_exists(self):
        note_label = mixer.blend(Label, id=1)
        assert note_label.is_label_instance == True

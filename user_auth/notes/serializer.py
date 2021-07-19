from rest_framework import serializers
from .models import NewNotes


class NotesSer(serializers.ModelSerializer):
    # serializer class for Notes database
    class Meta:
        model = NewNotes
        fields = "__all__"


class NotesUpdateSer(serializers.ModelSerializer):
    # specific serializer class for updating notes in database
    class Meta:
        model = NewNotes
        fields = ["id", "title", "discription"]



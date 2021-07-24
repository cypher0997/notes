from rest_framework import serializers
from .models import NewNotes, Label


class NotesSer(serializers.ModelSerializer):
    # serializer class for Notes database
    class Meta:
        model = NewNotes
        exclude = ["label"]


class NotesGetSer(serializers.ModelSerializer):
    class Meta:
        model = NewNotes
        fields = "__all__"


class NotesUpdateSer(serializers.ModelSerializer):
    # specific serializer class for updating notes in database
    class Meta:
        model = NewNotes
        fields = ["id", "title", "discription", "label"]


class LabelSer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = "__all__"

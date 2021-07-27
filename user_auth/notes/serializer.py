from rest_framework import serializers
from .models import NewNotes, Label, CollaboratorContent


class NotesSer(serializers.ModelSerializer):
    # serializer class for Notes database
    class Meta:
        model = NewNotes
        exclude = ["label", "collaborator"]


class NotesGetSer(serializers.ModelSerializer):
    # serializer class for Notes database
    class Meta:
        model = NewNotes
        fields = "__all__"


class NotesUpdateSer(serializers.ModelSerializer):
    # serializer class for Notes database
    # specific serializer class for updating notes in database
    class Meta:
        model = NewNotes
        fields = ["id", "title", "discription", "label"]


class LabelSer(serializers.ModelSerializer):
    # serializer class for Label database
    class Meta:
        model = Label
        fields = "__all__"


class CollaboratorContentSer(serializers.ModelSerializer):
    # serializer class for Notes CollaboratorContent
    class Meta:
        model = CollaboratorContent
        fields = "__all__"

    # def validate_(self, attrs):

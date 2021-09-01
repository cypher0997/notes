from rest_framework import serializers
from .models import Notes, Label


class NotesSer(serializers.ModelSerializer):
    # serializer class for Notes database
    title = serializers.CharField(max_length=200, allow_blank=True)
    description = serializers.CharField(max_length=200, allow_blank=True)

    class Meta:
        model = Notes
        exclude = ["label", "collaborator"]


class NotesGetSer(serializers.ModelSerializer):
    # serializer class for Notes database

    class Meta:
        model = Notes
        fields = "__all__"


class NotesUpdateSer(serializers.Serializer):
    # serializer class for Notes database
    # specific serializer class for updating notes in database
    title = serializers.CharField(max_length=200, allow_blank=True)
    description = serializers.CharField(max_length=200, allow_blank=True)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class LabelSer(serializers.ModelSerializer):
    # serializer class for Label database
    class Meta:
        model = Label
        fields = "__all__"



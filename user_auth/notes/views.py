from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from notes.models import NewNotes, Label
from notes.serializer import NotesSer, NotesUpdateSer, LabelSer, NotesGetSer
from rest_framework.response import Response
from uer_register_login.models import CustomUser
from uer_register_login.utils import token_decoder
import redis


class CreateNotes(APIView):

    # this class represent different views that are broadly different operations performed vis this api

    @token_decoder
    def get(self, request):
        """
        this method presents various notes of corresponding user
        :param request: http request to made to this api
        :return: it returns response to request that is made
        """
        try:
            usr_id = request.data.get("user")
            note = NewNotes.objects.filter(user=usr_id)
            serializer = NotesGetSer(data=note, many=True)
            serializer.is_valid()
            r = redis.Redis(host='localhost', port=6379, db=0)
            sr = serializer.data
            return Response({"data": {"note-list": sr},
                             "username": r.get("usr_name"),
                             "user_id": r.get("usr_id")}, status=200)
        except Exception as e:
            return Response({"message": e.args})

    @token_decoder
    def post(self, request):
        """
        this method used to create notes of corresponding user
        :param request: http request to made to this api
        :return: it returns response to request that is made
        """
        try:
            usr_id = request.data.get("user")
            label = Label.objects.get(label_name=request.data.get("label"))
            print(label)
            user = CustomUser.objects.get(id=usr_id)
            new_note = NewNotes(user=user, title=request.data.get("title"),
                                discription=request.data.get("discription"))
            serializer = NotesSer(new_note)
            deserialized_data = NotesSer(data=serializer.data)
            if deserialized_data.is_valid():
                deserialized_data.save()
                print(deserialized_data.data)
                pass
            else:
                return Response({"error": "note not serialized"})
            retrieve = NewNotes.objects.get(title=deserialized_data.data.get("title"))
            print(retrieve)
            retrieve.label.add(label)
            retrieve.save()
            return Response({"message": "NOTES CREATED"}, status=200)
        except Exception as e:
            return Response({"message": str(e)})

    def put(self, request):
        """
        this method updates specific notes of corresponding user
        :param request: http request to made to this api
        :return: it returns response to request that is made:
        """
        try:
            note_id = request.data.get("id")
            note = NewNotes.objects.get(pk=note_id)
            serializer = NotesUpdateSer(note, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "USER UPDATED SUCCESSSFULLY"})
            return Response(serializer.errors)
        except Exception as e:
            return Response({"message": str(e)})

    def delete(self, request):
        """
        this method delete's specific notes of corresponding user
        :param request: http request to made to this api
        :return: it returns response to request that is made:
        :param pk: primary representing user
        """
        try:
            input_id = request.data.get("id")
            user = NewNotes.objects.filter(pk=input_id)
            user.delete()
            return Response({"message": "NOTE SUCCESSFULLY DELETED"})
        except Exception as e:
            return Response({"message": e.args})


class LabelView(APIView):

    def post(self, request):
        label = Label(label_name=request.data.get("label"))
        label_serializer = LabelSer(label)
        label_deserializer = LabelSer(data=label_serializer.data)
        if label_deserializer.is_valid():
            label_deserializer.save()
            return Response({"message": "label created"}, status=200)
        else:
            return Response("something went wrong")

    def delete(self, request):
        try:
            label_id = request.data.get("id")
            label = Label.objects.filter(pk=label_id)
            label.delete()
            return Response({"message": "LABEL SUCCESSFULLY DELETED"})
        except Exception as e:
            return Response({"message": e.args})

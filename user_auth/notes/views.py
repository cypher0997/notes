from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from notes.models import NewNotes
from notes.serializer import NotesSer, NotesUpdateSer
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
            usr_id = request.data.get("id")
            data = NewNotes.objects.filter(user=usr_id)
            serializer = NotesSer(data=data, many=True)
            serializer.is_valid()
            r = redis.Redis(host='localhost', port=6379, db=0)
            return Response({"data": {"note-list": serializer.data},
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
            usr_id = request.data.get("id")
            user = CustomUser.objects.get(id=usr_id)
            # if request.data.get("title") or request.data.get("discription") is None:
            #     raise ValueError
            new_note = NewNotes(user=user, title=request.data.get("title"),
                                discription=request.data.get("discription"))
            serializer = NotesSer(new_note)
            deserialized_data = NotesSer(data=serializer.data)
            deserialized_data.is_valid()
            deserialized_data.save()
            print(user)
            return Response({"message": "NOTES CREATED"}, status=200)
        except ValueError as e:
            return Response({"message": "INVALID INPUT"}, status=400)
        except Exception as e:
            return Response({"message": str(e)})

    @token_decoder
    def put(self, request):
        """
        this method updates specific notes of corresponding user
        :param request: http request to made to this api
        :return: it returns response to request that is made:
        :param pk: primary representing user
        """
        try:
            # if request.data.get("title") or request.data.get("discription") is None:
            #     raise ValueError
            input_id = request.data.get("id")
            user = NewNotes.objects.get(pk=input_id)
            print(request.data)
            serializer = NotesUpdateSer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "USER UPDATED SUCCESSSFULLY"})
            return Response(serializer.errors)
        # except ValueError as e:
        #     return Response({"message": "INVALID INPUT"}, status=400)
        except Exception as e:
            return Response({"message": e.args})

    @token_decoder
    def delete(self, request):
        """
        this method delete's specific notes of corresponding user
        :param request: http request to made to this api
        :return: it returns response to request that is made:
        :param pk: primary representing user
        """
        try:
            input_id = request.data.get("id")
            user = NewNotes.objects.get(pk=input_id)
            user.delete()
            return Response({"message": "NOTE SUCCESSFULLY DELETED"})
        except Exception as e:
            return Response({"message": e.args})

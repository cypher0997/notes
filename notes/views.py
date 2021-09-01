from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
from jwt import ExpiredSignatureError
from rest_framework.views import APIView
from notes.models import Notes, Label
from notes.serializer import NotesSer, NotesUpdateSer, LabelSer, NotesGetSer
from rest_framework.response import Response
from uer_register_login.models import CustomUser
from uer_register_login.utils import token_decoder
from drf_yasg import openapi
from notes.utils import notes_log


class CreateNotes(APIView):
    # this class represent different views that are broadly different operations performed vis this api

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('AUTHORIZATION', openapi.IN_HEADER, "token to get user id", type=openapi.TYPE_STRING), ])
    @token_decoder
    def get(self, request):
        """
        this method presents various notes of corresponding user
        :param request: http request to made to this api
        :return: it returns response to request that is made
        """
        try:

            usr_id = request.data.get("user")
            note = Notes.objects.filter(user=usr_id)
            collaborator = Notes.objects.filter(collaborator=usr_id)
            note_serializer = NotesGetSer(data=note, many=True)
            coll_serializer = NotesGetSer(data=collaborator, many=True)
            note_serializer.is_valid()
            coll_serializer.is_valid()
            note_data = note_serializer.data
            coll_data = coll_serializer.data
            return Response({"data": {"note-list": note_data,
                                      "coll_list": coll_data}}, status=200)
        except ObjectDoesNotExist as e:
            notes_log.exception("object not found exception occurred")
            return Response({"message": str(e)}, status=404)
        except ValidationError as e:
            notes_log.exception("data validation failed exception occurred")
            return Response({"message": e.message}, status=400)
        except Exception as e:
            notes_log.exception("generic exception occurred")
            return Response({"message": e.args}, status=402)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING, description="title of note"),
            'description': openapi.Schema(type=openapi.TYPE_STRING, description="description of Note"),
            'label': openapi.Schema(type=openapi.TYPE_STRING, description="label of Note"),
        }), manual_parameters=[
        openapi.Parameter('AUTHORIZATION', openapi.IN_HEADER, "token to get user id", type=openapi.TYPE_STRING), ])
    @token_decoder
    def post(self, request):
        """
        this method used to create notes of corresponding user
        :param request: http request to made to this api
        :return: it returns response to request that is made
        """
        try:
            label = None
            usr_id = request.data.get("user")
            if request.data.get("label"):
                label = Label.objects.get(label_name=request.data.get("label"))
            user = CustomUser.objects.get(id=usr_id)
            new_note = Notes(user=user, title=request.data.get('title'),
                             description=request.data.get("description"))
            serializer = NotesSer(new_note)
            deserialized_data = NotesSer(data=serializer.data)
            if deserialized_data.is_valid():
                deserialized_data.save()
            if not deserialized_data.is_valid():
                return Response({"error": "note not serialized"}, status=400)
            if label is not None:
                retrieve = Notes.objects.latest("id")
                retrieve.label.add(label)
                retrieve.save()
                return Response({"message": "NOTE CREATED"}, status=200)
            return Response({"message": "NOTE CREATED"}, status=200)
        except ObjectDoesNotExist as e:
            notes_log.error("object not found exception occurred")
            return Response({"message": "EITHER LABEL OR USER OR ANY ONE OF REQUIRED FILED NOT FOUND"}, status=404)
        except ExpiredSignatureError as e:
            notes_log.error("token not found exception occurred")
            return Response({"message": "Token Not Found or expired"}, status=404)
        except Exception as e:
            notes_log.error("generic exception occurred")
            return Response({"message": str(e)})

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'note_id': openapi.Schema(type=openapi.TYPE_STRING, description="id of note"),
            'title': openapi.Schema(type=openapi.TYPE_STRING, description="title of note"),
            'description': openapi.Schema(type=openapi.TYPE_STRING, description="description of Note"),
            'label': openapi.Schema(type=openapi.TYPE_STRING, description="label of Note"),
        }), manual_parameters=[
        openapi.Parameter('AUTHORIZATION', openapi.IN_HEADER, "token to get user id", type=openapi.TYPE_STRING), ])
    def put(self, request):
        """
        this method updates specific notes of corresponding user
        :param request: http request to made to this api
        :return: it returns response to request that is made:
        """
        try:
            if not request.data.get("note_id"):
                notes_log.error("invalid input data")
                return Response({"message": "invalid input"})
            note = Notes.objects.get(pk=request.data.get("note_id"))
            serializer = NotesUpdateSer(note, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "NOTE UPDATED SUCCESSFULLY"})
            return Response(serializer.errors)
        except ObjectDoesNotExist as e:
            notes_log.exception("object not found exception occurred")
            return Response({"message": "NOTE NOT FOUND"}, status=404)
        except ValidationError as e:
            notes_log.exception("data validation failed")
            return Response({"message": str(e)})
        except Exception as e:
            notes_log.exception("generic exception occurred")
            return Response({"message": str(e)})

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_STRING, description="title of note"),
        }), manual_parameters=[
        openapi.Parameter('AUTHORIZATION', openapi.IN_HEADER, "token to get user id", type=openapi.TYPE_STRING), ])
    def delete(self, request):
        """
        this method delete's specific notes of corresponding user
        :param request: http request to made to this api
        :return: it returns response to request that is made:
        """
        try:
            if not request.data.get("id"):
                notes_log.error("invalid input data")
                return Response({"message": "invalid input"})
            input_id = request.data.get("id")
            user = Notes.objects.filter(pk=input_id)
            user.delete()
            return Response({"message": "NOTE SUCCESSFULLY DELETED"})
        except ObjectDoesNotExist as e:
            notes_log.exception("object not found exception occurred")
            return Response({"message": str(e)})
        except Exception as e:
            notes_log.exception("generic exception occurred")
            return Response({"message": e.args})


class LabelView(APIView):

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'label': openapi.Schema(type=openapi.TYPE_STRING, description="label"),
        }))
    def post(self, request):
        """
        post method for creating label
        :param request: incoming request
        :return: Response to give
        """
        try:
            if not request.data.get("label"):
                notes_log.error("invalid input data")
                return Response({"message": "invalid input"})
            label = Label(label_name=request.data.get("label"))
            label_serializer = LabelSer(label)
            label_deserializer = LabelSer(data=label_serializer.data)
            if label_deserializer.is_valid():
                label_deserializer.save()
                return Response({"message": "label created"}, status=200)
            return Response({"message": "Label Not Serialised"}, status=400)
        except ValidationError as e:
            notes_log.exception("data validation failed")
            return Response({"message": str(e)})
        except Exception as e:
            notes_log.exception("generic exception occurred")
            return Response({"message": e.args})


class NoteCollaboratorView(APIView):

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'note_id': openapi.Schema(type=openapi.TYPE_STRING, description="id of note"),
            'username': openapi.Schema(type=openapi.TYPE_STRING, description="USERNAME to  be collaborated"),
        }), manual_parameters=[
        openapi.Parameter('AUTHORIZATION', openapi.IN_HEADER, "token to get user id", type=openapi.TYPE_STRING), ])
    @token_decoder
    def post(self, request):
        """
        post method for creating collaborator
        :param request: incoming request
        :return: Response to give
        """
        try:
            if (not request.data.get("note_id")) or (not request.data.get("username")):
                notes_log.error("invalid input data")
                return Response({"message": "invalid input"})
            note = Notes.objects.get(pk=request.data.get("note_id"))
            collaborator = CustomUser.objects.get(username=request.data.get("username"))
            usr_id = request.data.get("user")
            user = CustomUser.objects.get(id=usr_id)
            if user:
                if collaborator:
                    if Notes.objects.filter(collaborator__id=collaborator.pk):
                        return Response({"message": "collaborator already exists"}, status=400)
                    else:
                        note.collaborator.add(collaborator.id)
                        note.save()
                        return Response({"message": "collaborator created"}, status=200)
                else:
                    return Response({"message": "User(want to be collaborator) not exists in DataBase"})
            else:
                return Response({"message": "USER HAS NOT PROPERLY LOGGED IN"})
        except ObjectDoesNotExist as e:
            notes_log.exception("object not found exception occurred")
            return Response({"message": "COLLABORATOR NOT FOUND"}, status=404)
        except Exception as e:
            notes_log.exception("generic exception occurred")
            return Response({"message": str(e)})

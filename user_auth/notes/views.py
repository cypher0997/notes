from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
from jwt import ExpiredSignatureError
from rest_framework.views import APIView
from notes.models import NewNotes, Label, CollaboratorContent
from notes.serializer import NotesSer, NotesUpdateSer, LabelSer, NotesGetSer, CollaboratorContentSer
from rest_framework.response import Response
from uer_register_login.models import CustomUser
from uer_register_login.utils import token_decoder
from drf_yasg import openapi


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
            note = NewNotes.objects.filter(user=usr_id)
            coll = NewNotes.objects.filter(collaborator=usr_id)
            print(coll)
            serializer = NotesGetSer(data=note, many=True)
            serializer.is_valid()
            note_sr = serializer.data
            serializer = NotesGetSer(data=coll, many=True)
            serializer.is_valid()
            coll_sr = serializer.data
            # coll_content = CollaboratorContent.objects.all().order_by('- id')
            # coll_serializer = CollaboratorContentSer(data=coll_content, many=True)
            # coll_serializer.is_valid()
            # content_sr = coll_serializer.data
            return Response({"data": {"note-list": note_sr,
                                      "coll_list": coll_sr}})

        except ObjectDoesNotExist as e:
            return Response({"message": str(e)})
        except ValidationError as e:
            return Response(e.message)
        except Exception as e:
            return Response({"message": e.args})

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING, description="title of note"),
            'discription': openapi.Schema(type=openapi.TYPE_STRING, description="discription of Note"),
            'label': openapi.Schema(type=openapi.TYPE_STRING, description="label of Note"),
        }) ,manual_parameters=[
        openapi.Parameter('AUTHORIZATION', openapi.IN_HEADER, "token to get user id", type=openapi.TYPE_STRING), ])
    @token_decoder
    def post(self, request):
        """
        this method used to create notes of corresponding user
        :param request: http request to made to this api
        :return: it returns response to request that is made
        """
        try:
            usr_id = request.data.get("user")
            print(usr_id)
            label = Label.objects.get(label_name=request.data.get("label"))
            user = CustomUser.objects.get(id=usr_id)
            print(user)
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
        except ObjectDoesNotExist as e:
            return Response({"message": "EITHER LABEL OR USER OR ANY ONE OF REQUIRED FILED NOT FOUND"}, status=404)
        except ExpiredSignatureError as e:
            return Response({"message": "Token Not Found or expired"}, status=404)
        except Exception as e:
            return Response({"message": str(e)})

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_STRING, description="title of note"),
            'title': openapi.Schema(type=openapi.TYPE_STRING, description="title of note"),
            'discription': openapi.Schema(type=openapi.TYPE_STRING, description="discription of Note"),
        }), manual_parameters=[
        openapi.Parameter('AUTHORIZATION', openapi.IN_HEADER, "token to get user id", type=openapi.TYPE_STRING),])
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
                return Response({"message": "USER UPDATED SUCCESSFULLY"})
            return Response(serializer.errors)
        except ObjectDoesNotExist as e:
            return Response({"message": "USER NOT FOUND"}, status=404)
        except ValidationError as e:
            return Response({"message": str(e)})
        except Exception as e:
            return Response({"message": str(e)})

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_STRING, description="title of note"),
        }), manual_parameters=[
        openapi.Parameter('AUTHORIZATION', openapi.IN_HEADER, "token to get user id", type=openapi.TYPE_STRING),])
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
        except ObjectDoesNotExist as e:
            return Response({"message": str(e)})
        except Exception as e:
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
            label = Label(label_name=request.data.get("label"))
            label_serializer = LabelSer(label)
            label_deserializer = LabelSer(data=label_serializer.data)
            if label_deserializer.is_valid():
                label_deserializer.save()
                return Response({"message": "label created"}, status=200)
            else:
                return Response("something went wrong")
        except ValidationError as e:
            return Response({"message": str(e)})
        except Exception as e:
            return Response({"message": e.args})

    def delete(self, request):
        """
        delete method  to delete label
        :param request: incoming request
        :return: Response to give
        """
        try:
            label_id = request.data.get("id")
            label = Label.objects.filter(pk=label_id)
            label.delete()
            return Response({"message": "LABEL SUCCESSFULLY DELETED"})
        except Exception as e:
            return Response({"message": e.args})


class NoteCollaboratorView(APIView):

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'note_id': openapi.Schema(type=openapi.TYPE_STRING, description="id of note"),
            'username': openapi.Schema(type=openapi.TYPE_STRING, description="USERNAME to  be collaborated"),
        }))
    def post(self, request):
        """
        post method for creating collaborator
        :param request: incoming request
        :return: Response to give
        """
        try:
            note = NewNotes.objects.get(pk=request.data.get("note_id"))
            collaborator = CustomUser.objects.get(username=request.data.get("username"))
            if collaborator:
                if NewNotes.objects.filter(collaborator__id=collaborator.pk):
                    return Response({"message": "collaborator already exists"}, status=400)
                else:
                    note.collaborator.add(collaborator.id)
                    note.save()
                    return Response({"message": "collaborator created"}, status=200)
        except ObjectDoesNotExist as e:
            return Response({"message": "COLLABORATOR NOT FOUND"}, status=404)
        except Exception as e:
            return Response({"message": str(e)})


class CollaboratedContentView(APIView):

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'note_id': openapi.Schema(type=openapi.TYPE_STRING, description="id of note"),
            'content': openapi.Schema(type=openapi.TYPE_STRING, description="content of collaborator"),
        }), manual_parameters=[
        openapi.Parameter('AUTHORIZATION', openapi.IN_HEADER, "token to get user id", type=openapi.TYPE_STRING),])
    @token_decoder
    def put(self, request):
        """
        post method for creating collaborator content
        :param request: incoming request
        :return: Response to give
        """
        try:
            collaborator = CustomUser.objects.get(pk=request.data.get("user"))
            note = NewNotes.objects.get(pk=request.data.get("note_id"))
            con = request.data.get("content")
            content = CollaboratorContent(note_id=note, collaborator_id=collaborator,
                                          content=con)
            serialize = CollaboratorContentSer(content)
            deserialize = CollaboratorContentSer(data=serialize.data)
            if deserialize.is_valid():
                if NewNotes.objects.filter(collaborator__id=collaborator.pk):
                    content.save()
                    if NewNotes.objects.filter(pk=request.data.get("note_id")).filter(collaborator__id=collaborator.pk):
                        note.discription = con
                        note.save()
                    return Response({"message": "saved"}, status=200)
            return Response({"message": "Not saved"}, status=200)
        except ValidationError as e:
            return Response({"message": str(e)})
        except ObjectDoesNotExist as e:
            return Response({"message": "USER NOT FOUND"}, status=404)
        except Exception as e:
            return Response({"message": str(e)})

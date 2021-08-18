from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.CreateNotes.as_view(), name='notes'),
    path('label/', views.LabelView.as_view(), name='label'),
    path('coll/', views.NoteCollaboratorView.as_view(), name='collaborator'),
]

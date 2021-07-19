from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.CreateNotes.as_view(), name='notes')
]
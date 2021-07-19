from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name="login_method"),
    path('reg/', views.RegisterView.as_view(), name="register_method"),
    path('verify/<str:token>', views.VerifyView.as_view(), name="verify_method")

]

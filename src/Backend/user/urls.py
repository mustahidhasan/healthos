from django.conf import settings
from django.urls import path
from django.views.static import serve
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from .views import ChangePrimaryPhoneNumber, Login, Register, CreateCompany, CreatePhoneNumber
urlpatterns = [
    path('login/', Login.as_view()),
    path('registration/', Register.as_view()),
    path('create/company/', CreateCompany.as_view()),
    path('create/phonenumber/', CreatePhoneNumber.as_view()),
    path('change/primary/phonenumber/', ChangePrimaryPhoneNumber.as_view()),

]

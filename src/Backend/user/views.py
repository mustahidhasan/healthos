import json
import random
import sys
import time

import requests
from django.contrib.auth.models import update_last_login
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
# email
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.utils.html import strip_tags


# Create your views here.
from rest_framework import status, generics
from rest_framework.generics import RetrieveAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.auth import EmailOrUsernameModelBackend
from user.models import *
from user.serializers import LoginSerializer, JWT_PAYLOAD_HANDLER, JWT_ENCODE_HANDLER, UserDetailSerializer, RegisterSerializer, CreateCompanySerializer
# Create your views here.

# register user


class Register(APIView):
    serializer_class = RegisterSerializer

    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            if not User.objects.filter(usr_email=request.data['usr_email']):
                serializer = self.serializer_class(data=request.data)
                is_vaid = serializer.is_valid(raise_exception=True)
                if is_vaid:
                    serializer.save()
                    response = {
                        'success': 'True',
                        'status code': status.HTTP_200_OK,
                        'message': 'Registration has been Successful.',
                        'data': serializer.data
                    }

                    return Response(response)
                else:
                    response = {
                        'success': 'False',
                        'status code': status.HTTP_400_BAD_REQUEST,
                        'message': 'Invalid Serializer',
                        'data': serializer.data
                    }
            else:
                response = {
                    'success': 'True',
                    'status code': status.HTTP_200_OK,
                    'message': 'Email Already Exist'
                }
                return Response(response)
        except Exception as e:
            response = 'on line {}'.format(
                sys.exc_info()[-1].tb_lineno), str(e)
            return Response(response, status=status.HTTP_201_CREATED)

# login user


class Login(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        print(request.data)
        response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': 'User logged in  successfully',
        }
        user_data = User.objects.filter(Q(usr_email=request.data.get('usr_email')) | Q(
            username=request.data.get('usr_email'))).first()
        if user_data is None:
            response['success'] = 'False'
            response['status code'] = status.HTTP_404_NOT_FOUND
            response['message'] = "User Not Found"
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        elif user_data.is_active == 1 and user_data.is_verify == 1:
            auth_user = EmailOrUsernameModelBackend.authenticate(user_data, username=request.data.get('usr_email'),
                                                                 password=request.data.get('password'))
            if auth_user is None:
                response['success'] = "False"
                response['status code'] = status.HTTP_400_BAD_REQUEST
                response['message'] = "Wrong Credentials"
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                try:
                    payload = JWT_PAYLOAD_HANDLER(auth_user)
                    jwt_token = JWT_ENCODE_HANDLER(payload)
                    groups = []
                    group_list = auth_user.groups.all()
                    for group in group_list.iterator():
                        groups.append(group.name)
                    update_last_login(None, auth_user)
                    response['success'] = 'True'
                    response['user_id'] = auth_user.id
                    response['token'] = jwt_token
                    response['groups'] = json.dumps(groups)
                    response['status code'] = status.HTTP_200_OK
                    response['user_data'] = UserDetailSerializer(
                        User.objects.get(Q(username=request.data['usr_email']) | Q(usr_email=request.data['usr_email']))).data
                    response['message'] = 'User Logged in'
                    return Response(response, status=status.HTTP_200_OK)
                except User.DoesNotExist:
                    response['success'] = 'False'
                    response['status code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
                    response['message'] = 'Internal Server Error'
                    return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            response['success'] = 'False'
            response['status code'] = status.HTTP_403_FORBIDDEN
            response['message'] = 'User is not approved yet. Please wait for admin approval.'
            return Response(response, status=status.HTTP_403_FORBIDDEN)

# create a company


class CreateCompany(APIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CreateCompanySerializer

    def post(self, request):
        try:
            if not Company.objects.filter(company_name=request.data['company_name']):
                serializer = self.serializer_class(data=request.data)
                is_vaid = serializer.is_valid(raise_exception=True)
                if is_vaid:
                    serializer.save()
                    response = {
                        'success': 'True',
                        'status code': status.HTTP_200_OK,
                        'message': 'Company Creation successfull',
                        'data': serializer.data
                    }

                    return Response(response)
                else:
                    response = {
                        'success': 'False',
                        'status code': status.HTTP_400_BAD_REQUEST,
                        'message': 'Invalid Serializer',
                        'data': serializer.data
                    }
            else:
                response = {
                    'success': 'True',
                    'status code': status.HTTP_200_OK,
                    'message': 'Company Already Exist'
                }
                return Response(response)
        except Exception as e:
            response = 'on line {}'.format(
                sys.exc_info()[-1].tb_lineno), str(e)
            return Response(response, status=status.HTTP_201_CREATED)

# create a phone number


class CreatePhoneNumber(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):

        try:
            user_id = request.data.get('user')
            company_id = request.data.get('company')
            is_primary_phone = request.data.get('is_primary_phone')
            phone = generate_number()  # call the phone number generator funciton
            if not UserCompanyManager.objects.filter(phn_cell=phone):
                get_phone_number_company_wise = UserCompanyManager.objects.create(
                    user_id=user_id,
                    company_id=company_id,
                    is_primary_phone=is_primary_phone,
                    phn_cell=phone
                )
                if get_phone_number_company_wise:
                    response = {
                        'success': 'True',
                        'status code': status.HTTP_200_OK,
                        'message': 'Company Wise Phone Number Creation successfull',
                    }

                    return Response(response)
                else:
                    response = {
                        'success': 'False',
                        'status code': status.HTTP_400_BAD_REQUEST,
                        'message': 'Company Wise Phone Number Creation unsuccessfull',
                    }
                return Response(response)
            else:
                return CreatePhoneNumber
        except Exception as e:
            response = 'on line {}'.format(
                sys.exc_info()[-1].tb_lineno), str(e)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

# change the primary number


class ChangePrimaryPhoneNumber(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        phone_number = request.data.get('phone_number')
        is_primary_phone = request.data.get('is_primary_phone')
        if UserCompanyManager.objects.filter(phn_cell=phone_number):
            get_company = UserCompanyManager.objects.filter(
                phn_cell=phone_number
            ).values()
            # change the other primary number false
            for idx in get_company:
                UserCompanyManager.objects.filter(
                    company_id=idx['company_id']
                ).update(
                    is_primary_phone="False"
                )
            # update the selected number to primary
            update_primary_phone_number = UserCompanyManager.objects.filter(
                phn_cell=phone_number
            ).update(
                is_primary_phone=is_primary_phone
            )
            if update_primary_phone_number:
                response = {
                    'success': 'True',
                    'status code': status.HTTP_200_OK,
                    'message': 'Primary Phone Number changed',
                }
            else:
                response = {
                    'success': 'False',
                    'status code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Primary Phone Number not changed',
                }
            return Response(response)
        else:
            response = {
                'success': 'False',
                'status code': status.HTTP_404_NOT_FOUND,
                'message': 'Phone number not found',
            }
        return Response(response)

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
from user.models import *
from dataplan.models import *
from datetime import datetime, timedelta
from dateutil.relativedelta import *
# Create your views here.

class AddDataPlan(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        plan_name = request.data.get('plan_name')
        plan_duration = request.data.get('plan_duration')
        plan_amt = request.data.get('plan_amt')
        is_plan_cancel_able = request.data.get('is_plan_cancel_able')

        try:
            create_data_plan = DataPlan.objects.create(
                plan_name = plan_name,
                duration_in_month = plan_duration,
                plan_amt = plan_amt,
                is_cancel_able = is_plan_cancel_able,
            )
            if create_data_plan:
                response = {
                    'success': 'True',
                    'status code': status.HTTP_200_OK,
                    'message': "Data plan created",
                }
            else:
                response = {
                    'success': 'True',
                    'status code': status.HTTP_200_OK,
                    'message': "Data plan created",
                }
            return Response(response)
        except Exception as e:
            response = 'on line {}'.format(
                sys.exc_info()[-1].tb_lineno), str(e)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class AddPlan(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        bd_time = datetime.now()

        phone_number = request.data.get('phone_number')
        plan_id = request.data.get('plan_id')

        get_user_manager = UserCompanyManager.objects.filter(
            phn_cell=phone_number,
            is_primary_phone=True,
        ).values()
        
        if get_user_manager:
            for idx in get_user_manager:
                # if the plan is cancleable or not
                is_cancleable = DataPlan.objects.filter(
                    id=plan_id).values_list('is_cancel_able').last()[0]
                print("line 54", is_cancleable)
                # is there any active plan 
                if Purches.objects.filter(company_id = idx['company_id']):
                    is_there_any_active_plan = Purches.objects.filter(
                        company_id = idx['company_id'],
                    ).values_list('active_plan').last()[0]
                    try:
                        # no activat plan for this company
                        if not is_there_any_active_plan:
                            # not cancle able plans
                            if not is_cancleable:
                                get_plan_duration = DataPlan.objects.filter(
                                    id=plan_id).values_list('duration').first()[0]
                                
                                # define the end date time
                                ending_datetime = bd_time + \
                                    relativedelta(months=+get_plan_duration)

                                # not cancle able data plan purches
                                Purches.objects.create(
                                    user_id=idx['user_id'],
                                    company_id=idx['company_id'],
                                    data_plan_id=plan_id,
                                    data_plan_ended=ending_datetime,
                                    active_plan=True

                                )
                            else:
                                # cancleable plans
                                Purches.objects.create(
                                    user_id=idx['user_id'],
                                    company_id=idx['company_id'],
                                    data_plan_id=plan_id,
                                    active_plan=True

                                )
                            response = {
                                'success': 'True',
                                'status code': status.HTTP_200_OK,
                                'message': get_user_manager,
                            }
                            return Response(response)
                        else:
                            response = {
                            'success': 'False',
                            'status code': status.HTTP_403_FORBIDDEN,
                            'message': 'Already have an active plan',
                            }
                            return Response(response)
                    except Exception as e:
                        response = 'on line {}'.format(
                            sys.exc_info()[-1].tb_lineno), str(e)
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)
                else:
                    try:
                        # not cancle able plans
                        if not is_cancleable:
                            get_plan_duration = DataPlan.objects.filter(
                                id=plan_id).values_list('duration').first()[0]
                            
                            # define the end date time
                            ending_datetime = bd_time + \
                                relativedelta(months=+get_plan_duration)
                            # not cancle able data plan purches
                            Purches.objects.create(
                                user_id=idx['user_id'],
                                company_id=idx['company_id'],
                                data_plan_id=plan_id,
                                data_plan_ended=ending_datetime,
                                active_plan=True
                            )
                        else:
                            # cancleable plans
                            Purches.objects.create(
                                user_id=idx['user_id'],
                                company_id=idx['company_id'],
                                data_plan_id=plan_id,
                                active_plan=True
                            )
                        response = {
                            'success': 'True',
                            'status code': status.HTTP_200_OK,
                            'message': get_user_manager,
                        }
                        return Response(response)
                    except Exception as e:
                        response = 'on line {}'.format(
                            sys.exc_info()[-1].tb_lineno), str(e)
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            if UserCompanyManager.objects.filter(phn_cell=phone_number):
                response = {
                    'success': 'False',
                    'status code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Phone number is not a primary number, please change the number to primary',
                }
            else:
                response = {
                    'success': 'False',
                    'status code': status.HTTP_404_NOT_FOUND,
                    'message': 'Phone number not found',
                }

            return Response(response)

class CanclePlan(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        active_plan_id = request.data.get('active_plan_id')
        try:
            # if any active plan exists
            if Purches.objects.filter(id = active_plan_id,active_plan=True):

                # getting the cancleable active plan id
                get_active_cancle_able_plan_id = Purches.objects.filter(
                id = active_plan_id,
                active_plan=True,
                ).values_list(
                    'data_plan_id'
                ).first()[0]
                # checking the plan is cancleable or not
                check_if_the_data_plan_is_cancle_able = DataPlan.objects.filter(
                    id =get_active_cancle_able_plan_id
                ).values_list('is_cancel_able').first()[0]

                if check_if_the_data_plan_is_cancle_able:
                    # canceling the plan if its cancleable
                    cancle_the_plan = Purches.objects.filter(
                        id = active_plan_id
                    ).update(
                        active_plan=False
                    )
                    if cancle_the_plan:
                        response = {
                            'success': 'True',
                            'status code': status.HTTP_200_OK,
                            'message': "Plan Cancled",
                        }
                    else:
                        response = {
                        'success': 'False',
                        'status code': status.HTTP_400_BAD_REQUEST,
                        'message': "Failed",
                    }

                else:
                    response = {
                        'success': 'False',
                        'status code': status.HTTP_404_NOT_FOUND,
                        'message': "Cancleable Plan Not Found",
                    }
                return Response(response)
            else:
                response = {
                        'success': 'False',
                        'status code': status.HTTP_404_NOT_FOUND,
                        'message': "No active plan found",
                    }
                return Response(response)
        except Exception as e:
                response = 'on line {}'.format(
                    sys.exc_info()[-1].tb_lineno), str(e)
                return Response(response, status=status.HTTP_400_BAD_REQUEST)



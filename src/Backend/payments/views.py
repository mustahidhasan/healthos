import stripe
from django.conf import settings
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
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

stripe.api_key = 'sk_test_51MREJLSJ58IUkqiHUoHQtjPDyg9NHgkHsOJ1NQtGWpCmHKIjH4TDCj3tGiI9LfWFfPqiNbEOCl0ZRL0gt3rZPBYO001nqfeCKF'


class CreateCheckoutSession(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            print("hi")
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "id": "prod_NBvr56WMtlvljd",
                        "object": "product",
                        "active": True,
                        "attributes": [
                        ],
                        "created": 1674034336,
                        "default_price": "price_1MRY0DSJ58IUkqiHtL97SssK",
                        "description": None,
                        "images": [
                        ],
                        "livemode": False,
                        "metadata": {
                        },
                        "name": "myplan",
                        "owning_merchant": "acct_1MREJLSJ58IUkqiH",
                        "owning_merchant_info": "acct_1MREJLSJ58IUkqiH",
                        "package_dimensions": None,
                        "shippable": None,
                        "skus": {
                            "object": "list",
                            "data": [
                            ],
                            "has_more": False,
                            "total_count": 0,
                            "url": "/v1/skus?product=prod_NBvr56WMtlvljd&active=true"
                        },
                        "statement_descriptor": None,
                        "tax_code": None,
                        "type": "service",
                        "unit_label": None,
                        "updated": 1674034339,
                        "url": None,
                        "user_hidden_in_lists": False
                    }
                ],
                mode='payment',
                success_url=True,
                cancel_url=True
                )
            print("line 58", checkout_session)
            response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': "checkout_session",
        }
        except Exception as e:
            response = {
            'success': 'False',
            'status code': status.HTTP_400_BAD_REQUEST,
            'message': str(e),
        }

        return Response(response)
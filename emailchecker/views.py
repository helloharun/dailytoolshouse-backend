from django.http.response import HttpResponse
from django.shortcuts import render
from validate_email import validate_email_or_fail
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from helpers.mixins import APIMixin

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.exceptions import Throttled
from rest_framework import status

from rest_framework.throttling import UserRateThrottle

@method_decorator(csrf_exempt, name='dispatch')
class EmailChecker(APIMixin, APIView):

   # per-view throttling
   throttle_classes = [UserRateThrottle]
   def post(self, request, format=None):
      try:
         email_id = request.data['email_id']
      except Exception as e:
         return self.error_response({
                  'msg':f'{e} missing'
               })
      responses = {

      }
      try:
         is_valid = validate_email_or_fail(
         email_address=email_id,
         check_format=True,
         check_blacklist=True,
         check_dns=True,
         dns_timeout=10,
         check_smtp=True,
         smtp_timeout=10,
         smtp_helo_host='smtp.gmail.com',
         smtp_from_address='loipofaw@gmail.com',
         smtp_skip_tls=False,
         smtp_tls_context=None,
         smtp_debug=False
         )
         print('is_valid:::::::::', is_valid)
         if is_valid:
            responses['msg'] = 'Valid email'
            responses['status'] = 200
      except Exception as e:
         responses['msg'] = f'{e}'
         responses['status'] = 400
      return Response(responses)

   def throttled(self, request, wait):
      print(request)
      raise Throttled(
         detail={
            "message":"Too many request",
            "available_in":f"{wait} seconds",
            "status_code": status.HTTP_429_TOO_MANY_REQUESTS
         }
      )

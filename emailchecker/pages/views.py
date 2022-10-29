from django.shortcuts import render, HttpResponse
from emailchecker.views import EmailChecker
import requests
from django.views import View
from django.http import JsonResponse
import json
from django.contrib import messages
from django.conf import settings

class EmailCheckerHome(View):
   # Global variables
   access_tokens = dict()
   
   @property
   def get_access_token(self):

      url = settings.EMAIL_CHECKER_ACCESS_TOKEN_URL
      payload = {
         'email':settings.USER_EMAIL,
         'password':settings.USER_PASSWORD
      }
      res = requests.post(url, data=payload)
      
      parsed_res = json.loads(res.content.decode())

      # setting access_tokens
      self.access_tokens['data'] = parsed_res

      return JsonResponse({'data': parsed_res},safe=False)
   
   # print('access_tokens: ', access_tokens)
   
   def get(self, request):
      self.get_access_token
      return render(request, 'email-checker-home.html')

   def validate_raw_email(self, raw_email):
      # initializing access_token variable
      access_token = ''

      try:
         access_token = self.access_tokens['data']['access']
      except:
         self.get_access_token
         
      if access_token == '':
         self.get_access_token
      
      # email checker API end point
      url = settings.EMAIL_CHECKER_URL

      # Data
      headers = {
         'Authorization': f'Bearer {access_token}',
      }
      
      payload = {
         'email_id':raw_email
      }

      try:
         res = requests.post(url, data=payload, headers=headers)
      except Exception as e:
         print("error:", e)
      
      parsed_email_response = json.loads(res.content.decode())
      return JsonResponse({'data': parsed_email_response},safe=False)


   def post(self, request):
      # catch email from post request
      raw_email = request.POST.get('raw-email')

      # calling validation_response method for email validation
      validation_response = self.validate_raw_email(raw_email)
      
      # parsing the response
      parsed_validation_response = json.loads(validation_response.content.decode())

      try:
         if str(parsed_validation_response['data']['status']) == '200':
            messages.success(request, parsed_validation_response['data']['msg'], extra_tags='Congratulations!')
         elif str(parsed_validation_response['data']['status']) == '400':
            messages.error(request, parsed_validation_response['data']['msg'], extra_tags='Oops!')
         else:
            messages.error(request, parsed_validation_response['data']['msg'], extra_tags='Error!')
      except Exception as e:
         if parsed_validation_response['data']['code'] == 'token_not_valid':
            return self.get(request)

      # return HttpResponse("Email Checker Home")
      return render(request, 'email-checker-home.html')
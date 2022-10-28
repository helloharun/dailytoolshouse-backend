from os import access
from django.shortcuts import render, HttpResponse
from emailchecker.views import EmailChecker
import requests
from django.views import View
from django.http import JsonResponse
import json
from django.contrib import messages


class EmailCheckerHome(View):
   # Global variables
   access_tokens = dict()
   
   @property
   def get_access_token(self):
      url = 'http://127.0.0.1:8000/tpauth/get_token/'
      payload = {
         'email':'test@dailytoolshouse.com',
         'password':'asdf@123'
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

   def post(self, request):
      access_token = self.access_tokens['data']['access']
      
      raw_email = request.POST.get('raw-email')
      
      url = 'http://127.0.0.1:8000/email-checker/checker/'

      headers = {
         'Authorization': f'Bearer {access_token}',
      }
      
      payload = {
         'email_id':raw_email
      }


      res = requests.post(url, data=payload, headers=headers)
      
      parsed_email_response = json.loads(res.content.decode())
      if str(parsed_email_response['status']) == '200':
         messages.success(request, parsed_email_response['msg'], extra_tags='Congratulations!')
      elif str(parsed_email_response['status']) == '400':
         messages.error(request, parsed_email_response['msg'], extra_tags='Oops!')

      # return HttpResponse("Email Checker Home")
      return render(request, 'email-checker-home.html')
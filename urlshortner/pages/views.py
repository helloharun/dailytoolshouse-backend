from django.views import View
from django.shortcuts import render, HttpResponse, redirect
from django.conf import settings
import requests
import json
from django.http.response import JsonResponse
from django.contrib import messages
from helpers.mixins import APIMixin

'''
Here, the concept is that the "pages" is a client of urlshortner app so its working accordingly.
'''

def get_access_token():
      url = settings.EMAIL_CHECKER_ACCESS_TOKEN_URL
      payload = {
         'email':settings.USER_EMAIL,
         'password':settings.USER_PASSWORD
      }
      res = requests.post(url, data=payload)
      
      parsed_res = json.loads(res.content.decode())

      # # setting access_tokens
      # self.access_tokens['data'] = parsed_res

      return JsonResponse({'data': parsed_res},safe=False)

class URLHome(View):
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
   
   def get(self, request):
      self.get_access_token
      print('access_tokens: ', self.access_tokens)
      return render(request, 'urlshortner_home.html')

   def post(self, request):
      long_url = request.POST.get('long-url', None)

      url = 'http://127.0.0.1:8000/url-shortner/api/create/'

      headers = {
         'Authorization': 'Bearer '+self.access_tokens['data']['access']
      }

      payload = {
         'requested_url': long_url
      }

      res = requests.post(url, data=payload, headers=headers)

      print('res:::', json.loads(res.content.decode()))

      parsed_res = json.loads(res.content.decode())
      if parsed_res['status'] ==  200:
         messages.success(request, {'msg':parsed_res['data']['msg'],'generated_url':parsed_res['data']['generated_url'], 'requested_url':parsed_res['data']['requested_url']}, extra_tags='Congratulations!')
      elif parsed_res['status'] ==  400:
         messages.error(request, {'msg':parsed_res['errors']['msg'],'generated_url':None, 'requested_url':parsed_res['errors']['requested_url']}, extra_tags='Oops!')
      return render(request, 'urlshortner_home.html')

class URLCheck(View, APIMixin):
   def get(self, request, url_query):

      # if len(url_query) < 7 or len(url_query) > 9:
      #    raise ValueError("url_query is invalid")

      http_host = self.request.__dict__['META']['HTTP_HOST']
      req_url = http_host+"/"+url_query+"/"

      if len(url_query) < 7 or len(url_query) > 10:
         messages.error(request, {'msg':'URL could be invalid!','requested_url':req_url}, extra_tags='Oops!')
      else:
         try:
            # Token Generation
            access_token_data = get_access_token()
            parsed_access_token_data = json.loads(access_token_data.content.decode())
            access_token = parsed_access_token_data['data']['access']

            url = 'http://127.0.0.1:8000/url-shortner/api/url-id/checker/'

            headers = {
               'Authorization': 'Bearer '+access_token
            }

            payload = {
               'requested_short_url': url_query
            }

            res = requests.post(url, data=payload, headers=headers)

            # print('res:::', json.loads(res.content.decode()))

            parsed_res = json.loads(res.content.decode())

            print('::::::::::parsed_res::::::::::::::', parsed_res)
            
            if parsed_res['status'] == 200:
               # return HttpResponseRedirect(parsed_res['data']['original_url'])
               return redirect(parsed_res['data']['original_url'])
            else:
               messages.error(request, {'msg':parsed_res['errors']['msg'],'requested_url':req_url}, extra_tags='Oops!')
            
         except Exception as e:
            print('Exception e: ', e)

      return render(request, 'urlshortner_home.html')

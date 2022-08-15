from django.shortcuts import render
from django.http import JsonResponse, HttpRequest
import string
import random
from .models import UrlsBook
from rest_framework import viewsets
from .serializers import UrlsBookSerializer
from django.shortcuts import redirect
import urllib
from rest_framework.permissions import IsAuthenticated
from helpers.mixins import APIMixin
from helpers.helpers import success_response, error_response
from rest_framework.decorators import api_view

from rest_framework.throttling import AnonRateThrottle
from rest_framework.exceptions import Throttled
from rest_framework import status

class UrlBookViewset(viewsets.ModelViewSet, APIMixin):
   queryset = UrlsBook.objects.all()
   serializer_class = UrlsBookSerializer
   throttle_classes = [AnonRateThrottle]

   def create(self, request):
      requested_url = request.data['requested_url']
      
      # Validating the requested URLs
      parsed_url = urllib.parse.urlparse(requested_url)
      parsed_url_scheme = parsed_url.scheme
      print('parsed_url_scheme: ', parsed_url_scheme)
      parsed_url_netloc = parsed_url.netloc
      print('parsed_url_netloc: ', parsed_url_netloc)
      parsed_url_path = parsed_url.path
      print('parsed_url_path: ', parsed_url_path)

      if parsed_url_scheme != '' and parsed_url_netloc != '' and parsed_url_path != '':
         chars = string.ascii_letters + string.digits
         length_options = [7,8,9,10]
         generated_keys = ''.join(random.choice(chars) for i in range(random.choice(length_options)))
         domain_name = request.META['HTTP_HOST']
         url_scheme = request.META['wsgi.url_scheme']
         # print('request.META :', request.META)
         generated_url = url_scheme+'://'+domain_name +'/'+generated_keys

         to_be_saved_url = UrlsBook.objects.create(requested_url=requested_url, generated_url=generated_url, key=generated_keys)
         to_be_saved_url.save()
         return self.success_response({
            'msg':'URL shortner successful','generated_url':generated_url, 'requested_url':requested_url,
            })
      else:
         return self.error_response({
            'msg':'URL shortner failed. There could be some issues on provided URLs.', 'requested_url':requested_url,
            })
      
   def harun(self, request):
      return self.success_response({'msg':'Hi Harun'})
   
   def throttled(self, request, wait):
      raise Throttled(
         detail = {
            "message":"Too many request",
            "available_in":f"{wait} seconds",
            "status_code": status.HTTP_429_TOO_MANY_REQUESTS
         }
      )
      
@api_view(['GET'])
def URLRedirect(request, **kwargs):
   requested_key = kwargs.get('key')
   try:
      filtered_key = UrlsBook.objects.get(key=requested_key)
      filtered_requested_url = filtered_key.__dict__['requested_url']

      return redirect(filtered_requested_url)
   except Exception as e:
      return error_response({'msg': f'{e}', 'code':'401'})
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

from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.exceptions import Throttled
from rest_framework import status
from rest_framework.views import APIView


class UrlBook(APIMixin, APIView):
   throttle_classes = [UserRateThrottle]

   def post(self, request):
      
      # comes from the request
      requested_url = request.POST.get('requested_url',None)

      if requested_url is not None:
         
         # Validating the requested URLs
         parsed_url = urllib.parse.urlparse(requested_url)
         parsed_url_scheme = parsed_url.scheme
         # print('parsed_url_scheme: ', parsed_url_scheme)
         parsed_url_netloc = parsed_url.netloc
         # print('parsed_url_netloc: ', parsed_url_netloc)
         parsed_url_path = parsed_url.path
         # print('parsed_url_path: ', parsed_url_path)

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
               'msg':'URL shortner successful',
               'generated_url':generated_url, 
               'requested_url':requested_url,
               })
         else:
            return self.error_response({
               'msg':'URL shortner failed. There could be some issues on provided URLs.', 'requested_url':requested_url,
               })
      else:
         raise ValueError("long URL or requested_url cannot be None")
      
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

class UrlChecker(APIMixin, APIView):

   throttle_classes = [UserRateThrottle]
   def post(self, request, *agrs, **kwargs):

      # requested_short_url = request.POST.get('requested_short_url', None)

      # getting request shortened URL from clients
      requested_short_url = request.data.get('requested_short_url', None)

      '''
      # key for filtering
      url_key = str()
      if requested_short_url is not None:
         
         # disecting the shortened URLs
         parsed_url = urllib.parse.urlparse(requested_short_url)

         
         parsed_url_scheme = parsed_url.scheme
         # print('parsed_url_scheme: ', parsed_url_scheme)
         parsed_url_netloc = parsed_url.netloc
         # print('parsed_url_netloc: ', parsed_url_netloc)
         parsed_url_path = parsed_url.path
         # print('parsed_url_path: ', parsed_url_path)

         if parsed_url_scheme == '':
            return self.error_response({
               'msg':'Incorrect requested short URL.',
               'requested_short_url':requested_short_url, 
               })
         elif parsed_url_netloc == '':
            return self.error_response({
               'msg':'Incorrect requested short URL.',
               'requested_short_url':requested_short_url, 
               })
         elif parsed_url_path == '':
            return self.error_response({
               'msg':'Incorrect requested short URL.',
               'requested_short_url':requested_short_url, 
               })
         elif len(parsed_url_path[1:]) < 7 or len(parsed_url_path[1:]) > 10:
            return self.error_response({
               'msg':'Incorrect requested short URL.',
               'requested_short_url':requested_short_url, 
               })
         else:
            url_key = parsed_url_path[1:]

      else:
         return self.error_response({
            'msg':'Requested short URL cannot be empty!'
            })
      '''
      
      url_key = requested_short_url
      try:
         filtered_key = UrlsBook.objects.get(key=url_key)
         filtered_key.click_counts += 1
         filtered_key.save() #saves the click counts
         filtered_requested_url = filtered_key.__dict__['requested_url']

         return self.success_response({
            'msg':'Request short URL found successfully!',
            'requested_short_url': requested_short_url,
            'original_url': filtered_requested_url
         })
      except Exception as e:
         return error_response({'msg': f'{e}', 'requested_short_url':requested_short_url})
      
   def throttled(self, request, wait):
      raise Throttled(
         detail = {
            "message":"Too many request",
            "available_in":f"{wait} seconds",
            "status_code": status.HTTP_429_TOO_MANY_REQUESTS
         }
      )
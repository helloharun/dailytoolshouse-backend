from django.shortcuts import render
from django.http import JsonResponse

import json


def home(request):
   # service_dict = dict()
   service_dict = {"data":[
      {
         "service_name":"Password Generator",
         "description":"Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.",
         "image_url":"images/password-generator.jpg",
         "service_details_urls":"passwordGenerator"
      },
      {
         "service_name":"Email Checker",
         "description":"Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.",
         "image_url":"images/email_checker.jpg",
         "service_details_urls":"emailchecker-page-home"
      },
      {
         "service_name":"Documents Converter",
         "description":"Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.",
         "image_url":"images/document-convertor.jpg",
         "service_details_urls":"home"
      }]    
      }
      
   return render(request, 'dthhome.html', context=service_dict)
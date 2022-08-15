from rest_framework import status
from rest_framework.response import Response

def success_response(data={}, status=status.HTTP_200_OK):
   if isinstance(data, str):
      data = {'detail': data}
   payload = {
      'success': True,
      'status': status,
      'data': data or {
         'detail':'Request Successful'
         }
   }

   return Response(payload, status=status)

def error_response(data={}, status=status.HTTP_400_BAD_REQUEST, error_code='dailytoolshouse _error'):
   if isinstance(data, str):
      data = {'detail': data}
   payload = {
      'success': False,
      'status': status,
      'errors': data or {
         'detail': 'Something went wrong'
      }
   }

   payload['errors']['error_code']=error_code

   return Response(payload, status=status)

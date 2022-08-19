from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .helpers import success_response, error_response

class APIMixin:
   # lookup_field = 'uid'
   permission_classes = [IsAuthenticated]
   # authentication_classes = []

   def success_response(self, data={}, status=status.HTTP_200_OK):
      return success_response(data=data, status=status)
   
   def error_response(self, data={}, status=status.HTTP_400_BAD_REQUEST, error_code='dailytoolshouse_error'):
      return error_response(data=data, status=status, error_code=error_code)

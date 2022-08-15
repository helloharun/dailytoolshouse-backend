from rest_framework import serializers
from .models import UrlsBook

class UrlsBookSerializer(serializers.ModelSerializer):
   class Meta:
      model = UrlsBook
      fields = ['uid','requested_url','is_deleted','created_on','modified_on']
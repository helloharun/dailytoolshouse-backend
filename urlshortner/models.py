from django.db import models
from helpers.models import BaseModel
# Create your models here.
class UrlsBook(BaseModel):
   requested_url = models.CharField(max_length=255)
   generated_url = models.CharField(max_length=200)
   key = models.CharField(max_length=200, unique=True)


from django.db import models
import uuid

# Create your models here.
class BaseModel(models.Model):
   uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
   created_on = models.DateTimeField(auto_now_add=True)
   modified_on = models.DateTimeField(auto_now=True)
   is_deleted = models.BooleanField(default=False)

   class Meta:
      abstract = True
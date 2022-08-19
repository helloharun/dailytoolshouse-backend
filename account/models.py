from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.expressions import Value
from django.utils.translation import ugettext_lazy as _
from rest_framework.response import Response

from helpers.models import BaseModel
import uuid

class AccountManager(BaseUserManager):
   def _create_user(self, mobile, email, password, **extra_fields):
      '''
      Create and save a user with the provided email, mobile, and the password
      '''
      if not email:
         raise ValueError(_('Email must be set'))
      email = self.normalize_email(email)
      user = self.model(mobile=mobile, email=email, **extra_fields)
      user.set_password(password)
      user.save(using=self._db)
      return user
   
   def create_user(self, mobile, email, password, **extra_fields):
      extra_fields.setdefault('is_active', False)
      extra_fields.setdefault('is_staff', False)
      extra_fields.setdefault('is_superuser', False)
      extra_fields.setdefault('is_verified', False)
      return self._create_user(mobile, email, password, **extra_fields)
   
   def create_superuser(self, mobile, email, password, **extra_fields):
      extra_fields.setdefault('is_active', True)
      extra_fields.setdefault('is_staff', True)
      extra_fields.setdefault('is_superuser', True)
      extra_fields.setdefault('is_verified', False)

      if extra_fields.get('is_staff') is not True:
         raise ValueError(_('Superuser must have is_staff=True'))
      if extra_fields.get('is_superuser') is not True:
         raise ValueError(_('Superuser must have is_superuser=True'))
      return self._create_user(mobile, email, password, **extra_fields)

class Account(AbstractBaseUser, PermissionsMixin, BaseModel):
   mobile = models.CharField(_('mobile'), max_length=15, unique=True)
   email = models.EmailField(_('email address'), unique=True)
   is_active = models.BooleanField(default=False)
   is_staff = models.BooleanField(default=False)
   is_superuser = models.BooleanField(default=False)
   is_verified = models.BooleanField(default=False)
   objects = AccountManager()
   USERNAME_FIELD = 'email'
   REQUIRED_FIELDS = ['mobile']

   def __str__(self):
      return self.email


   

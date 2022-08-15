from django.contrib import admin
from .models import Account

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
   list_display = ['email','mobile','is_active','is_staff','is_superuser','is_verified','is_deleted']
   search_fields = ['email','mobile']

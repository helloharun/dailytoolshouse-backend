from django.contrib import admin
from .models import UrlsBook

@admin.register(UrlsBook)
class UrlsBookAdmin(admin.ModelAdmin):
   list_display = ('uid','requested_url','generated_url','click_counts','key','is_deleted','created_on','modified_on')

# admin.site.register(UrlsBook)

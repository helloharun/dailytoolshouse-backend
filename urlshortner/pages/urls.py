from . import views
from django.urls import path

urlpatterns = [
   path('', views.URLHome.as_view(), name="url-shortner-home"),
   path('check/', views.URLCheck.as_view(), name="url-shortner-check")
]



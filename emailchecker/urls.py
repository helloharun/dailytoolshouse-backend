from django.urls import path
from . import views

urlpatterns = [
    path('checker/', views.EmailChecker.as_view(), name="email-checker"),
]
from django.urls import path

from emailchecker.pages import views

urlpatterns = [
   path('', views.EmailCheckerHome.as_view(), name="emailchecker-page-home")
]

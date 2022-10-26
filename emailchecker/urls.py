from django.urls import path, include
from . import views

urlpatterns = [
    path('checker/', views.EmailChecker.as_view(), name="email-checker"),
    path('pages/', include('emailchecker.pages.urls'))
]
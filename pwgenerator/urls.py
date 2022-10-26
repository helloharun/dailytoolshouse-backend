from django.urls import path, include

urlpatterns = [
   path('pages/', include("pwgenerator.pages.urls")),
]

from django.urls import path
from . import views

urlpatterns = [
   # path('single-generate/', views.SingleVideoGenerator, name="single-video-generator"),
   # path('single-download/', views.SingleVideoDownloader, name="single-video-downloader"),
   path('download/', views.OneHighestVideoDownloader, name="single-video-downloader")
]

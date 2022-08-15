from django.urls import path
from django.urls.conf import include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('app', views.UrlBookViewset, basename='url-app')
urlpatterns = [
   path('', include(router.urls)),
   path('harun/', views.UrlBookViewset.as_view({'get':'harun'}))
]

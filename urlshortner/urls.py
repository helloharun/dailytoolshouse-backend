from django.urls import path
from django.urls.conf import include
from . import views


urlpatterns = [
   path('api/create/', views.UrlBook.as_view(), name="url-book"),
   path('api/url-id/checker/', views.UrlChecker.as_view(), name="url-id-checker"),
   # path('harun/', views.UrlBookViewset.as_view({'get':'harun'})),
   path('pages/', include('urlshortner.pages.urls')),
]

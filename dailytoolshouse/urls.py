"""dailytoolshouse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from urlshortner.pages import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('email-checker/', include('emailchecker.urls')),
    path('video-downloader/', include('videodownloder.urls')),
    path('url-shortner/', include('urlshortner.urls')),
    path('tpauth/', include('tpauth.urls')),
    
    # for Home Page
    path('', include('home.urls')),

    # for Password generator
    path('pwgenerator/', include("pwgenerator.urls")),

    # for checking requested_shortened_url if exists
    path('<str:url_query>/', views.URLCheck.as_view(), name="client-url-checker"),



]

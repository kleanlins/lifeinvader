"""lifeinvader URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='start_page'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('success/', views.success, name='success'),
    path('profile_login/', views.user_login, name='user_login'),
    path('profile/', views.show_profile, name='show_profile'),
    path('home/', views.show_timeline, name='timeline'),
    path('profile/<int:id>/', views.visit_profile, name='visit_profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

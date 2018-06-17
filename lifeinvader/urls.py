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
    path('result/', views.success, name='success'),
    path('profile_login/', views.user_login, name='user_login'),
    path('profile/', views.show_profile, name='show_profile'),
    path('home/', views.show_timeline, name='timeline'),
    path('profile/<int:id>/', views.visit_profile, name='visit_profile'),
    path('group/<int:id>/', views.visit_group, name='visit_group'),
    path('group_created/', views.create_group, name='create_group'),
    path('gmanager/', views.group_manager, name='group_manager'),
    path('mmanager/', views.members_manager, name='members_manager'),
    path('maccepted/<int:id>/', views.accept_member, name='accept_member'),
    path('request_membership/<int:id>/', views.request_member, name='request_member'),
    path('removed_friend/', views.remove_friend, name='remove_friend'),
    path('added_friend/', views.add_friend, name='add_friend'),
    path('acced_friend/<int:id>/', views.acc_friend, name='acc_friend'),
    path('reffed_friend/<int:id>/', views.ref_friend, name='ref_friend'),
    path('login/', views.logout, name='logout'),
    path('delete_post_pr/<int:id>/', views.delete_post_pr, name='delete_post_pr'),
    path('answer_comment_tl/<int:id>/', views.answer_comment_tl, name='answer_comment_tl'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

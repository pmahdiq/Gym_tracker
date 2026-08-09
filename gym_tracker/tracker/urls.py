from django.contrib import admin
from django.urls import path

from .views import *


urlpatterns = [
    path('', dashboard_page, name='dashboard'),
    path('add_session', add_session_page,name='add_session'),
    path('edit_profile', edit_profile, name='edit_profile')
]
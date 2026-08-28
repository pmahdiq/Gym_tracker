from django.contrib import admin
from django.urls import path

from .views import *


urlpatterns = [
    path('dashboard', dashboard_page, name='dashboard'),
    path('add_program', add_program_page,name='add_program'),
    path('delete_program/<int:program_id>/', delete_program, name='delete_program'),
    path('edit_profile', edit_profile, name='edit_profile')
]
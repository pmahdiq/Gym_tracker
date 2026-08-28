from django.contrib import admin
from django.urls import path

from .views import *


urlpatterns = [
    path('dashboard', dashboard_page, name='dashboard'),
    path('add_program', add_program_page,name='add_program'),
    path('update_program/<int:program_id>/', update_program, name='update_program'),
    path('delete_program/<int:program_id>/', delete_program, name='delete_program'),
    path('start_session/<int:program_id>/', start_session, name='start_session'),
    path('session_history', session_history, name='session_history'),
    path('session_history/<int:session_id>/', session_detail, name='session_detail'),
    path('edit_profile', edit_profile, name='edit_profile')
]
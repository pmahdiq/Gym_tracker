from django.urls import path

from user_athentication.views import login_page

urlpatterns = [
    path('', login_page, name='login')
]
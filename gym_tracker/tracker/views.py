from django.shortcuts import render
from .models import Training_Program, Training_Session

def dashboard_page(request):
    training_programs = Training_Program.objects.all()
    sessions_count = Training_Session.objects.all().count()

    return render(request, 'tracker/dashboard.html',{
        'training_programs': training_programs,
        'sessions_count': sessions_count
        })

def add_session_page(request):
    return render(request, 'tracker/add_session.html')

def edit_profile(request):
    return render(request, 'tracker/edit_profile.html')
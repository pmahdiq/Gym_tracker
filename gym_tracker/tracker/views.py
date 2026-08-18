from django.utils import timezone
from django.shortcuts import render
from .models import Training_Program, Training_Session

def home_page(request):
    return render(request, 'tracker/home.html')

def dashboard_page(request):
    now = timezone.now()
    this_month_sessions_count = Training_Session.objects.filter(
        date_added__year=now.year,
        date_added__month=now.month
    ).count()
    training_programs = Training_Program.objects.all()
    sessions_count = Training_Session.objects.all().count()
    last_session_day = Training_Session.objects.all().order_by('date_added')[:1][0].date_added
    

    return render(request, 'tracker/dashboard.html',{
        'training_programs': training_programs,
        'sessions_count': sessions_count,
        'this_month_session_count': this_month_sessions_count,
        'last_session_day': last_session_day
        })

def add_session_page(request):
    return render(request, 'tracker/add_session.html')

def edit_profile(request):
    return render(request, 'tracker/edit_profile.html')
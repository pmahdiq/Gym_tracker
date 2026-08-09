from django.shortcuts import render

def dashboard_page(request):
    return render(request, 'tracker/dashboard.html')

def add_session_page(request):
    return render(request, 'tracker/add_session.html')

def edit_profile(request):
    return render(request, 'tracker/edit_profile.html')
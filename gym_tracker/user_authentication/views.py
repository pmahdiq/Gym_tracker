from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


def login_page(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')

                user = authenticate(request=request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'You loged in successfully')
                    return redirect('/tracker/')
            else:
                messages.error(request, 'Login failed')
    return render(request, 'user_authentication/login.html')

def register_page(request):
    if request.method == 'POST':
            user = UserCreationForm(request.POST)
    
            if user.is_valid():
                user.save()
                messages.success(request, "You sign up successfully.")
                return redirect('/authentication/login/')
            else:
                messages.error(request, 'Sign up failed')
            
    return render(request, 'user_authentication/register.html')

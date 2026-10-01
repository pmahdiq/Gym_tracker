from django import forms
from django.contrib.auth import authenticate

# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class Register_Form(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username']  # password1/password2 are added automatically by UserCreationForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Choose a username'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Create a strong password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm your password'})





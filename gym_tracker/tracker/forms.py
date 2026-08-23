from django import forms
from django.forms import inlineformset_factory

from tracker.models import Exercise, Training_Program

class Program_Model_Form(forms.ModelForm):
    class Meta:
        model = Training_Program
        fields = ['title', 'description']


Exercise_Form_Set = inlineformset_factory(
    Training_Program,
    Exercise,
    fields=["title"],
    extra=1,
    can_delete=True,
)
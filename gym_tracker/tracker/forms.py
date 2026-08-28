# forms.py
from django import forms
from tracker.models import Training_Program, Exercise


class Program_Model_Form(forms.ModelForm):
    class Meta:
        model = Training_Program
        fields = ['title', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'placeholder': 'Push Day'})
        self.fields['description'].widget.attrs.update({
            'placeholder': 'Optional notes about this program',
        })
        self.fields['description'].required = False


# One row per Exercise, linked to a TrainingProgram automatically.
# extra=1 gives you exactly the single starter row your JS then clones.
Exercise_Form_Set = forms.inlineformset_factory(
    Training_Program,
    Exercise,
    fields=['title'],
    extra=1,
    can_delete=False,
    widgets={
        'title': forms.TextInput(attrs={'placeholder': 'Bench Press'}),
    },
)

Session_Form_Set = forms.modelformset_factory(
    Exercise,
    fields=['sets', 'reps', 'weight'],
    extra=0,  # no blank rows — we're only editing existing exercises
    widgets={
        'sets': forms.NumberInput(attrs={'min': 1}),
        'reps': forms.NumberInput(attrs={'min': 1}),
        'weight': forms.NumberInput(attrs={'min': 0, 'step': 0.5}),
    },
)
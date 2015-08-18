from django import forms
from main.models import *

class TaskForm(forms.ModelForm):
    class Meta:
        model       = Task
        exclude     = [
            'user',
            'submitted_on',
            'status',
            'results_dir',
            'results'
        ]

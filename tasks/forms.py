from django.forms import ModelForm
from .models import Task
from django import forms

class TaskForm(ModelForm):
    class Meta:
        model=Task
        fields=['title', 'description', 'important']
        widgets={
            'title': forms.TextInput(attrs={'class':'form-control mb-2'}),
            'description': forms.Textarea(attrs={'class':'form-control mb-2'}),
            'important': forms.CheckboxInput(attrs={'class':'mb-2'})
        }
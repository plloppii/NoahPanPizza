from django import forms
from django.contrib.auth.models import User
from .models import Project

class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'project_type', 'content','images']

from django import forms
from django.contrib.auth.models import User
from .models import Project
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'content', 'thumbnail', 'tags', 'active', 'featured']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder':'Project Title'}),
            'project_type': forms.TextInput(attrs={'placeholder':'Project Meta Tags'}),
            'description': forms.Textarea(attrs={'rows':3, 'placeholder':'Project Description'}),
            'content': forms.Textarea(attrs={'placeholder':'Project Content Here!'})
        }
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_show_labels = False
            self.helper.form_method = 'POST'
            # self.helper.form_group_wrapper_class = 'row'
            # self.helper.label_class = 'offset-md-1 col-md-1'
            # self.helper.field_class = 'col-md-8'
            self.helper.add_input(Submit('submit', 'Submit'))

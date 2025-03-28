from django import forms
from .models import Teacher_ProfilePermission 

class Teacher_ProfilePermissionForm(forms.ModelForm):
    class Meta:
        model = Teacher_ProfilePermission
        fields = ['can_manage', 'can_create', 'can_edit', 'can_delete']
        

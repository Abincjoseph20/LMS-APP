from django import forms
from .models import Student_ProfilePermission
from adminapp.models import Account

class StudentProfilePermissionForm(forms.ModelForm):
    class Meta:
        model = Student_ProfilePermission
        fields = ['can_manage', 'can_create', 'can_edit', 'can_delete']
        
class StudentUserProfileForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'address', 'profile_image'] 
        # widgets = {
        #     'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
        #     'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
        #     'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
        #     'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}),
        #     'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
        #     'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your address', 'rows': 3}),
        #     'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
        # }       
# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from . models import Account

# class UserRegistrationForm(UserCreationForm):
#     email = forms.EmailField(required=True)

#     class Meta:
#         model = Account
#         fields = ['username', 'email', 'password1', 'password2', 'role']
        
        
        
        
# from django import forms
# from .models import Account

# class RegistrationForms(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput(attrs={
#         'placeholder':'Enter password',
#         'class':'form-control',
#     }))

#     confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
#         'placeholder':'Confirm password',
#         'class': 'form-control',
#     }))

#     class Meta:
#         model = Account
#         fields = ['first_name','last_name','phone_number','email','password']

#     def clean(self):
#         cleaned_data = super(RegistrationForms,self).clean()
#         password = cleaned_data.get('password')
#         confirm_password = cleaned_data.get('confirm_password')

#         if password != confirm_password:
#             raise forms.ValidationError(
#                 'password does not match!'
#             )


#     def __init__(self, *args, **kwargs):
#         super(RegistrationForms,self).__init__(*args,**kwargs)
#         self.fields['first_name'].widget.attrs['placeholder']='enter first name'
#         self.fields['last_name'].widget.attrs['placeholder']='last name'
#         self.fields['phone_number'].widget.attrs['placeholder']='phone number'
#         self.fields['email'].widget.attrs['placeholder']='email'

#         for field in self.fields:
#             self.fields[field].widget.attrs['class']='form-control'




from django import forms
from .models import Account

class RegistrationForms(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'password','roles']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Create a password'}),
            'roles': forms.Select(attrs={'class': 'form-control'}),
            }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match!")
        return cleaned_data




class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )
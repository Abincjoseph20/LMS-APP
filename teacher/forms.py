from django import forms
from .models import Teacher_ProfilePermission,Categories,Instructor,Levels,Language,Course

class Teacher_ProfilePermissionForm(forms.ModelForm):
    class Meta:
        model = Teacher_ProfilePermission
        fields = ['can_manage', 'can_create', 'can_edit', 'can_delete']
        

        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = '__all__'



class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = ['about_author', 'designation']        
        
        
        
class LevelForm(forms.ModelForm):
    class Meta:
        model = Levels
        fields = '__all__'
        
        
        
class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = '__all__'
        
        
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'featured_image', 'featured_video', 'title', 'category', 'level',
            'description', 'price', 'discount', 'language', 'deadline', 'slug',
            'status', 'Certificate', 'is_free'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'slug': forms.TextInput(attrs={'placeholder': 'Enter course slug'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Enter price'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CourseForm, self).__init__(*args, **kwargs)
        if user:
            pass
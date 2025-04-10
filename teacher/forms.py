from django import forms
from .models import Teacher_ProfilePermission,Categories,Instructor,Levels,Language,Course,Lessons,CourseResource,What_u_learn,Requirements,VideoModels

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
        
        
class LessonForm(forms.ModelForm):
    class Meta:
        model = Lessons
        fields = ['course', 'name']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter lesson name'
            }),
        }
   
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract the user passed during form initialization
        super().__init__(*args, **kwargs)
        if user:
            try:
                instructor = Instructor.objects.get(user=user)
                # Filter courses by the logged-in instructor
                courses = Course.objects.filter(author=instructor)
                if courses.exists():
                    self.fields['course'].queryset = courses
                else:
                    self.fields['course'].queryset = Course.objects.none()
                    self.fields['course'].empty_label = "No courses available"
                    self.fields['name'].widget.attrs['placeholder'] = "Please add a course first"

            except Instructor.DoesNotExist:
                # If the user is not an instructor, no courses are available
                self.fields['course'].queryset = Course.objects.none()
                self.fields['course'].empty_label = "No courses available"
                self.fields['name'].widget.attrs['placeholder'] =  'Author details not provided'
                
                
                

class CourseResourceForm(forms.ModelForm):
    class Meta:
        model = CourseResource
        fields = ['course', 'resource_type', 'title', 'file']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-select'}),
            'resource_type': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter resource title'
                }),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract the user passed during form initialization
        super().__init__(*args, **kwargs)
        if user:
            try:
                instructor = Instructor.objects.get(user=user)
                courses = Course.objects.filter(author=instructor)
                if courses.exists():
                    self.fields['course'].queryset = courses
                else:
                    self.fields['course'].queryset = Course.objects.none()
                    self.fields['course'].empty_label = "No courses available"  
                    self.fields['title'].widget.attrs['placeholder'] = "Please add a course first"   
            except Instructor.DoesNotExist:
                # If the user is not an instructor, no courses are available
                self.fields['course'].queryset = Course.objects.none()
                self.fields['course'].empty_label = "No courses available"
                self.fields['title'].widget.attrs['placeholder'] = "Author details not provided" 
                
                
                
                
class WhatULearnForm(forms.ModelForm):
    class Meta:
        model = What_u_learn
        fields = ['course', 'points']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-select'}),
            'points': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter points learned from the course'}),
        }



class RequirementsForm(forms.ModelForm):
    class Meta:
        model = Requirements
        fields = ['course', 'points']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-select'}),
            'points': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter requirement'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract the user passed during form initialization
        super().__init__(*args, **kwargs)
        if user:
            try:
                instructor = Instructor.objects.get(user=user)
                # Filter courses by the logged-in instructor
                courses = Course.objects.filter(author=instructor)
                if courses.exists():
                    self.fields['course'].queryset = courses
                else:
                    self.fields['course'].queryset = Course.objects.none()
                    self.fields['course'].empty_label = "No courses available"
                    self.fields['points'].widget.attrs['placeholder'] = "Please add a course first"
                        
            except Instructor.DoesNotExist:
                # If the user is not an instructor, no courses are available
                self.fields['course'].queryset = Course.objects.none()
                self.fields['course'].empty_label = "No courses available"
                self.fields['points'].widget.attrs['placeholder'] =  'Author details not provided'
                
                
                
class VideosForm(forms.ModelForm):
    class Meta:
        model = VideoModels
        fields = ['serial_number', 'thumbnail', 'course', 'lesson', 'title', 'video', 'time_duration', 'preview']
        widgets = {
            'serial_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter serial number'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
            'lesson': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter video title'}),
            'video': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Upload video'}),
            'time_duration': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter duration in seconds'}),
            'preview': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract the user passed during form initialization
        super().__init__(*args, **kwargs)
        if user:
            try:
                instructor = Instructor.objects.get(user=user)
                # Filter courses by the logged-in instructor
                courses = Course.objects.filter(author=instructor)
                if courses.exists():
                    self.fields['course'].queryset = courses
                    lessons = Lessons.objects.filter(course__in = courses)
                    if lessons.exists():
                        self.fields['lesson'].queryset = lessons
                    else:
                        self.fields['lesson'].empty_label = "Lessons not added"
                else:
                    self.fields['course'].queryset = Course.objects.none()
                    self.fields['course'].empty_label = "No courses available"
                    self.fields['lesson'].queryset = Lessons.objects.none()
                    self.fields['lesson'].empty_label = "Please add a course"
                    self.fields['title'].widget.attrs['placeholder'] = "Please add a course first"
                    

            except Instructor.DoesNotExist:
                # If the user is not an instructor, no courses are available
                self.fields['course'].queryset = Course.objects.none()
                self.fields['course'].empty_label = "No courses available"
                self.fields['lesson'].queryset = Lessons.objects.none()
                self.fields['lesson'].empty_label = "Please add a course"
                self.fields['title'].widget.attrs['placeholder'] =  'Author details not provided'
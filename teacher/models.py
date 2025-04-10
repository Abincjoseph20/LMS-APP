from django.db import models
from adminapp.models import Account  # Importing the Account model

class Teacher(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name="teacher_profile")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


# **Profile Permission Model**
class Teacher_ProfilePermission(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE,related_name="profile_permissions")
    can_manage = models.BooleanField(default=False)
    can_create = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.teacher.user.username} Profile Permissions"



class Categories(models.Model):
    icon = models.ImageField(upload_to="Media/icons")
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    def get_all_category(self):
        return Categories.objects.all().order_by('id')
    
class Instructor(models.Model):
    user = models.OneToOneField(Account,on_delete=models.CASCADE, related_name="instructor")  
    designation = models.CharField(max_length=100, null=True, blank=True)
    about_author = models.TextField()

    def __str__(self):
        return f"{self.user.username} - (Role: {self.designation})"

class Level(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    
    
    
class Levels(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    
class Language(models.Model):
    language = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.language
    
    
class Categories(models.Model):
    icon = models.ImageField(upload_to="Media/icons")
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    def get_all_category(self):
        return Categories.objects.all().order_by('id')    
    

class Course(models.Model):
    STATUS = (
        ('PUBLISH','PUBLISH'),
        ('DRAFT', 'DRAFT'),
    )

    featured_image = models.ImageField(upload_to="Media/featured_img",null=True)
    featured_video = models.CharField(max_length=300,null=True)
    title = models.CharField(max_length=500)
    created_at = models.DateField(auto_now_add=True)
    author = models.ForeignKey(Instructor,on_delete=models.CASCADE,null=True)
    category = models.ForeignKey(Categories,on_delete=models.CASCADE)
    level= models.ForeignKey(Levels,on_delete=models.CASCADE,null=True)
    description = models.TextField()
    price = models.IntegerField(null=True,default=0)
    discount = models.IntegerField(null=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True)
    deadline = models.CharField(max_length=100,null=True)
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)
    status = models.CharField(choices=STATUS,max_length=100,null=True)
    Certificate=models.CharField(null=True,max_length=100)
    is_free = models.BooleanField(default=False)  

    
    def __str__(self):
         return f"{self.title} - {self.language}"
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("course_detail", kwargs={'course_id': self.id})
    
#----NEW----#
    
class UserCourse(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    paid = models.BooleanField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Use getattr to provide default values if first_name or title is None
        user_name = getattr(self.user, 'username', 'No Name')
        course_title = getattr(self.course, 'title', 'No Title')
        return f"{user_name} - {course_title}"
    
class Lesson(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    
    def __str__(self):
        return self.name + " - " + self.course.title
    
class VideoModel(models.Model):  
    serial_number = models.IntegerField(null=True)
    thumbnail = models.ImageField(upload_to="Media/Yt_Thumbnail", null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    video = models.FileField(upload_to='course_videos/', null=True, blank=True)
    time_duration = models.IntegerField(null=True)
    preview = models.BooleanField(default=False)
    def __str__(self):
        return self.title 
    
    

    
    
    
class UserCourses(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    paid = models.BooleanField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Use getattr to provide default values if first_name or title is None
        user_name = getattr(self.user, 'username', 'No Name')
        course_title = getattr(self.course, 'title', 'No Title')
        return f"{user_name} - {course_title}"
    
# class Payment(models.Model):
#     user=models.ForeignKey(Account,on_delete=models.CASCADE)
#     course=models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
#     order_id = models.CharField(max_length=100,null=True,blank=True)
#     payment_id = models.CharField(max_length=100,null=True,blank=True)
#     user_course = models.ForeignKey(UserCourse,on_delete=models.CASCADE,null=True)
#     date= models.DateTimeField(auto_now_add=True)
#     status = models.BooleanField(default=False)

#     def __str__(self):
#         return self.user.first_name + " -- " + self.course.title  






class Lessons(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    
    def __str__(self):
        return self.name + " - " + self.course.title
    
    
    
# models
class CourseResource(models.Model):
    RESOURCE_TYPE = (
        ('Note', 'Note'),
        ('PDF', 'PDF'),
        ('PPT', 'PPT'),
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    resource_type = models.CharField(choices=RESOURCE_TYPE, max_length=10)
    title = models.CharField(max_length=500)
    file = models.FileField(upload_to="course_resources/",default='path/to/default/file.pdf')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    #   @classmethod
    def get_all_category(cls):
        return cls.objects.all()
    
    def __str__(self):
        return f"{self.title} - {self.resource_type} for {self.course.title}"
    
    
    
class What_u_learn(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    points=models.CharField(max_length=500)

    def __str__(self):
        return self.points
    
    
class Requirements(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    points=models.CharField(max_length=500) 

    def __str__(self):
        return self.points



class VideoModels(models.Model):  
    serial_number = models.IntegerField(null=True)
    thumbnail = models.ImageField(upload_to="Media/Yt_Thumbnail", null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    video = models.FileField(upload_to='course_videos/', null=True, blank=True)
    time_duration = models.IntegerField(null=True)
    preview = models.BooleanField(default=False)
    def __str__(self):
        return self.title 
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




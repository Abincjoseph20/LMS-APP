from django.db import models
from adminapp.models import Account  # Importing the Account model

class Parant(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name="parant_profile")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


# **Profile Permission Model**
class Parant_ProfilePermission(models.Model):
    student = models.ForeignKey(Parant, on_delete=models.CASCADE,related_name="profile_permissions")
    can_manage = models.BooleanField(default=False)
    can_create = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.user.username} Profile Permissions"

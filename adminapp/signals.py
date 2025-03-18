from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Account
from student.models import Student, Student_ProfilePermission

@receiver(post_save, sender=Account)
def create_student_profile(sender, instance, created, **kwargs):
    if created and instance.roles == 'student':
        Student.objects.create(user=instance)
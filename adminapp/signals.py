# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Account
# from student.models import Student, Student_ProfilePermission

# @receiver(post_save, sender=Account)
# def create_student_profile(sender, instance, created, **kwargs):
#     # if created and instance.roles == 'student':
#     if created and instance.roles in ['student', 'parent', 'guest']:
#         Student.objects.create(user=instance)
        
        
        
from django.db.models.signals import post_save
from django.dispatch import receiver
from adminapp.models import Account
from student.models import Student
from parant.models import Parant
from guest.models import Guest

@receiver(post_save, sender=Account)
def create_profile(sender, instance, created, **kwargs):
    # Ensure related model is created for superusers
    if created or instance.is_superadmin:
        if instance.roles == 'student':
            Student.objects.get_or_create(user=instance)
        elif instance.roles == 'parent':
            Parant.objects.get_or_create(user=instance)
        elif instance.roles == 'guest':
            Guest.objects.get_or_create(user=instance)

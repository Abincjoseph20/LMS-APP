from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Account
from student.models import Student, Student_ProfilePermission

@receiver(post_save, sender=Account)
def create_role_based_profile(sender, instance, created, **kwargs):
    """ Automatically creates a related profile based on the user role """
    if created:  # Only trigger when a new user is created
        if instance.roles == 'student':
            # Get the Student instance associated with the Account
            student_instance = Student.objects.filter(user=instance) 
            
            if student_instance and not Student_ProfilePermission.objects.filter(student=student_instance).exists():
                Student_ProfilePermission.objects.create(student=student_instance)
                
    print(f"Signal triggered for {instance.email} with role {instance.roles}")

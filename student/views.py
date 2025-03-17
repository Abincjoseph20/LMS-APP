from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import StudentProfilePermissionForm
from .models import Student_ProfilePermission, Student
from adminapp.models import Account

def assign_permissions(request, user_id):
    account = get_object_or_404(Account, id=user_id)  # Get the student by Account model
    student = get_object_or_404(Student, user=account) 

    if request.method == "POST":
        form = StudentProfilePermissionForm(request.POST)
        if form.is_valid():
            print(f"Updating permissions for {student}")
            # Retrieve or create permissions for the selected student
            permissions, created = Student_ProfilePermission.objects.get_or_create(student=student)
            permissions.can_manage = form.cleaned_data['can_manage']
            permissions.can_create = form.cleaned_data['can_create']
            permissions.can_edit = form.cleaned_data['can_edit']
            permissions.can_delete = form.cleaned_data['can_delete']
            permissions.save()
            print("Permissions saved successfully!")

            messages.success(request, f"Permissions assigned successfully to {account.first_name} {account.last_name}.")
            return redirect('success_page')  # Redirect to success page
        else:
            messages.error(request, "Failed to assign permissions. Please check the form.")

    else:
        # Prefill form with existing permissions if available
        existing_permissions = Student_ProfilePermission.objects.filter(student=student).first()
        form = StudentProfilePermissionForm(instance=existing_permissions)

    return render(request, 'student/student_roles_form.html', {'form': form, 'user': student})


def sucess(request):
    return render(request,'student/assign_permissions.html')

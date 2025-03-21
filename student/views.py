from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import StudentProfilePermissionForm
from .models import Student_ProfilePermission, Student
from adminapp.models import Account
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import StudentUserProfileForm
from adminapp.models import Account


def assign_permissions(request, user_id):
    account = get_object_or_404(Account, id=user_id)  # Get the student by Account model
    student = get_object_or_404(Student, user=account)
    
    try:
        student = Student.objects.get(user=account)
    except Student.DoesNotExist:
        student = None 

    if request.method == "POST":
        form = StudentProfilePermissionForm(request.POST)
        if form.is_valid():
            if student:
                print(f"Updating permissions for {student}")
                permissions, created = Student_ProfilePermission.objects.get_or_create(student=student)
            else:
                permissions, created = Student_ProfilePermission.objects.get_or_create(account=account)
            permissions.can_manage = form.cleaned_data['can_manage']
            permissions.can_create = form.cleaned_data['can_create']
            permissions.can_edit = form.cleaned_data['can_edit']
            permissions.can_delete = form.cleaned_data['can_delete']
            permissions.save()   
            print("Permissions saved successfully!")

            messages.success(request, f"Permissions assigned successfully to {account.first_name} {account.last_name}.")
            return redirect('success_page',user_id=user_id)  # Redirect to success page
        else:
            messages.error(request, "Failed to assign permissions. Please check the form.")
    else:
        existing_permissions = None
        if student:
            existing_permissions = Student_ProfilePermission.objects.filter(student=student).first()
        else:
            existing_permissions = Student_ProfilePermission.objects.filter(account=account).first()
        form = StudentProfilePermissionForm(instance=existing_permissions)

    return render(request, 'student/student_roles_form.html', {'form': form, 'user': student})


def success(request, user_id=None):
    student = None
    permissions = None
    
    if user_id:
        account = get_object_or_404(Account, id=user_id)
        
        # Ensure you correctly fetch the student object
        student = get_object_or_404(Student, user=account)

        # Fetch the permissions linked to the student
        permissions = Student_ProfilePermission.objects.filter(student=student).first()

    return render(request, 'student/assign_permissions.html', {
        'user': student,
        'permissions': permissions
    })


# @login_required
# def student_profile(request):
#     """ View to display and update user profile """
#     user = get_object_or_404(Account, id=id)  # Get the current logged-in user

#     if request.method == 'POST':
#         form = StudentUserProfileForm(request.POST, request.FILES, instance=user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Profile updated successfully.')
#             return redirect('student_profile', id=user.id)  # Redirect to the profile page after successful update
#         else:
#             messages.error(request, 'Please correct the errors below.')
#     else:
#         form = StudentUserProfileForm(instance=user)

#     return render(request, 'student/student_profile.html', {'form': form, 'user': user})



@login_required
def profile_edit(request):
    """ Edit user profile """
    if request.method == "POST":
        user = request.user

        # Update user fields
        user.username = request.POST.get('username', user.username)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.email = request.POST.get('email', user.email)
        user.phone_number = request.POST.get('phone_number', user.phone_number)
        user.address = request.POST.get('address', user.address)

        # Handle profile image upload
        if 'profile_image' in request.FILES:
            user.profile_image = request.FILES['profile_image']

        # Save the updated user data
        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('profile_view')

    return render(request, 'profile.html', {'user': request.user})


@login_required
def profile_delete(request):
    """ Delete user profile """
    user = request.user

    if request.method == "POST":
        user.delete()
        messages.success(request, "Profile deleted successfully!")
        return redirect('home')  # Redirect to home or login page after deletion

    return render(request, 'confirm_delete.html', {'user': user})
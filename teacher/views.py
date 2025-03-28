from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import  Teacher,Teacher_ProfilePermission
from adminapp.models import Account
from .forms import Teacher_ProfilePermissionForm 
from django.contrib.auth.decorators import login_required


def assign_teacher_permissions(request, user_id):
    account = get_object_or_404(Account, id=user_id)  
    teacher = get_object_or_404(Teacher, user=account)

    if request.method == "POST":
        form = Teacher_ProfilePermissionForm (request.POST)
        if form.is_valid():
            permissions, created = Teacher_ProfilePermission.objects.get_or_create(teacher=teacher)
            
            permissions.can_manage = form.cleaned_data['can_manage']
            permissions.can_create = form.cleaned_data['can_create']
            permissions.can_edit = form.cleaned_data['can_edit']
            permissions.can_delete = form.cleaned_data['can_delete']
            permissions.save()

            messages.success(request, f"Permissions assigned successfully to {account.first_name} {account.last_name}.")
            return redirect('teacher_success_page', user_id=user_id)  # Redirect to teacher success page
        else:
            messages.error(request, "Failed to assign permissions. Please check the form.")
    else:
        existing_permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
        form = Teacher_ProfilePermissionForm (instance=existing_permissions)

    return render(request, 'teacher/teacher_roles_form.html', {'form': form, 'user': teacher})

def teacher_success(request, user_id=None):
    teacher = None
    permissions = None

    if user_id:
        account = get_object_or_404(Account, id=user_id)
        teacher = get_object_or_404(Teacher, user=account)
        permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()

    return render(request, 'teacher/assign_permisssion.html', {
        'user': teacher,
        'permissions': permissions
    })



@login_required
def profile_edit(request):
    if request.method == "POST":
        user = request.user
        
        teacher = get_object_or_404(Teacher, user=user)
        permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
        
        # Check if the user has edit permissions
        if not permissions or not permissions.can_edit:
            messages.error(request, "You do not have permission to edit this profile.")
            return redirect('teacher_profile_view')
        
        # Handle profile image upload
        if 'profile_image' in request.FILES:
            user.profile_image = request.FILES['profile_image']
            user.save()
            messages.success(request, "Profile image updated successfully!")
            return redirect('teacher_profile_view')
        
        # Update user fields
        user.username = request.POST.get('username', user.username)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.email = request.POST.get('email', user.email)
        user.phone_number = request.POST.get('phone_number', user.phone_number)
        user.address = request.POST.get('address', user.address)

        # Save the updated user data
        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('teacher_profile_view')

    return render(request, 'profile.html', {'user': user})


@login_required
def profile_delete(request):
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.can_delete:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')

    if request.method == "POST":
        # Check if the confirmation checkbox is checked
        if 'confirm_delete' in request.POST:
            user.delete()
            messages.success(request, "Your account has been deleted successfully.")
            return redirect('register')  # Redirect to home or login page
        else:
            messages.error(request, "Please confirm the deletion before proceeding.")
            return redirect('profile_view')

    return render(request, 'confirm_delete.html', {'user': user})


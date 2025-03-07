from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.mail import send_mail
from django.conf import settings
from .models import Account
from .forms import RegistrationForms,LoginForm
import random
from django.contrib.auth import logout,authenticate
from .forms import LoginForm


def generate_otp():
    return str(random.randint(100000, 999999))  # 6-digit OTP

def register(request):
    if request.method == 'POST':
        form = RegistrationForms(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']  
            last_name = form.cleaned_data['last_name']    
            email = form.cleaned_data['email']
            role = form.cleaned_data['roles']
            print(email)
            password = form.cleaned_data['password']
            print(password)
            username = email.split('@')[0]
            
            # Ensure username is unique
            base_username = username.lower()
            unique_username = base_username
            counter = 1
            while Account.objects.filter(username=unique_username).exists():
                unique_username = f"{base_username}{counter}"
                counter += 1

            otp = generate_otp()

            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=unique_username,
                password=password,
                otp=otp,
                roles=role 
            )
            user.is_active = False  # user remains inactive until OTP verification
            user.save()

            # Send OTP to user's email
            try:
                send_mail(
                    subject="Your OTP Verification Code",
                    message=f"Your OTP for account activation is {otp}.",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                    fail_silently=False,
                )
                messages.success(request, 'OTP sent to your email. Verify your account.')
            except Exception as e:
                messages.error(request, f'Error sending OTP: {e}')
                return redirect('register')
            request.session['email'] = email
            return redirect('verify_otp')
    else:
        form = RegistrationForms()
    return render(request, 'registration/register.html', {'form': form})


def verify_otp(request):
    email = request.session.get('email')

    if not email:
        return redirect('register')

    if request.method == 'POST':
        otp_entered = request.POST.get('otp', '').strip()  
        try:
            user = Account.objects.get(email=email)
            print(f"Stored OTP in DB: {user.otp}")  # Debugging line
            print(f"User entered OTP: {otp_entered}")  # Debugging line
            
            if user.otp == otp_entered:
                user.is_active = True
                user.is_verified = True
                user.otp = None
                user.save()
                messages.success(request, 'Account verified successfully! Please log in.')
                return redirect('login')
                # return redirect('registration_success')
            else:
                messages.error(request, 'Invalid OTP. Try again.')
                print('Invalid OTP. Try again.')
        except Account.DoesNotExist:
            messages.error(request, 'User not found.')
            print('User not found')

    return render(request, 'registration/verify_otp.html')


def registration_success(request):
    return render(request, 'registration/success.html')


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            print(f'{email},{password}')
            
            # Use 'username' instead of 'email' for authentication
            user = authenticate(request, email=email, password=password)
            
            if user:
                if not user.is_verified:
                    messages.error(request, 'Please verify your account first.')
                    print('Please verify your account first.')
                    return redirect('login')  # Redirect immediately to prevent further execution
                
                auth.login(request, user)
                messages.success(request, 'You are now logged in.')
                
                # Redirect based on role
                if user.is_superadmin:
                    return redirect('admin_dashboard')
                elif user.roles == 'Teacher':
                    return redirect('teacher_dashboard')
                elif user.roles == 'student':
                    return redirect('student_dashboard')
                elif user.roles == 'Parent':
                    return redirect('parent_dashboard')  
                else:
                    return redirect('home')    
            else:
                messages.error(request, 'Invalid email or password.')
                print('Invalid email or password.') 
    else:
        form = LoginForm()   
    return render(request, 'registration/login1.html', {'form': form})




def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


def Home(request):
    return render(request,'base/home.html')


def admin_dashboard(request):
    return render(request, 'dashboard/admin_dashboard.html')

def teacher_dashboard(request):
    return render(request, 'dashboard/teacher_dashboard.html')

def student_dashboard(request):
    return render(request, 'dashboard/student_dashboard.html')

def parent_dashboard(request):
    return render(request, 'dashboard/parent_dashboard.html')

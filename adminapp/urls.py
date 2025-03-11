from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('login/', views.login, name='login'),
    # path('registration-success/', views.registration_success, name='registration_success'),
    path('logout/',views.logout_view, name='logout'),
    path('home/',views.Home, name='home'),
    
    
    path('admin_dashboard/',views.admin_dashboard, name='admin_dashboard'),
    path('teacher_dashboard/',views.teacher_dashboard, name='teacher_dashboard'),
    path('student_dashboard/',views.student_dashboard, name='student_dashboard'),
    path('parent_dashboard/',views.parent_dashboard, name='parent_dashboard'),
    
    
    
    path('all_users_list/', views.all_users_list, name='all_users_list'),
    path('roles/', views.roles, name='roles'),
    path('search_and_select/', views.search_and_select, name='search_and_select'),
    
    
    #profiles
    path('profile_view/', views.profile_view, name='profile_view'),
    path('profile_view/', views.profile_view, name='admin_profile'),
    path('student_profile/', views.profile_view, name='student_profile'),
    path('Teacher_profile/', views.profile_view, name='Teacher_profile'),
    path('guest_profile/', views.profile_view, name='guest_profile'),
    path('parant_profile/',views.profile_view,name='parant_profile')
    
]


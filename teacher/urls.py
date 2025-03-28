from django.urls import path
from . import views

urlpatterns = [

    path('teacher/assign_permissions/<int:user_id>/', views.assign_teacher_permissions, name='assign_teacher_permissions'),
    path('teacher/success_page/<int:user_id>/', views.teacher_success, name='teacher_success_page'),
    
    
    path('profile/edit/', views.profile_edit, name='teacher_profile_edit'),
    path('profile/delete/', views.profile_delete, name='teacher_profile_delete'),


]

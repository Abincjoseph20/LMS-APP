from django.urls import path
from . import views

urlpatterns = [
   path('assign_permissions/<int:user_id>/', views.student_assign_permissions, name='student_assign_permissions'),
   path('success_page/<int:user_id>/', views.student_success, name='student_success_page'),
   
   path('profile/edit/', views.profile_edit, name='profile_edit'),
   path('profile/delete/', views.profile_delete, name='profile_delete'),

]


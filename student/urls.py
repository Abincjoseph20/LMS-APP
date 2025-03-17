from django.urls import path
from . import views

urlpatterns = [
   path('assign_permissions/<int:user_id>/', views.assign_permissions, name='assign_permissions'),
   path('success_page/', views.sucess, name='success_page'),
    
]
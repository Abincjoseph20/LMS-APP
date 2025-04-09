from django.contrib import admin
from .models import Level

# Register your models here.

from.models import Teacher_ProfilePermission,Teacher

admin.site.register(Teacher_ProfilePermission) 
admin.site.register(Teacher) 
admin.site.register(Level)
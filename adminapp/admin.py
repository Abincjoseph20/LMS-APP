from django.contrib import admin
from.models import Account
# Register your models here.
class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'user_key', 'is_active', 'is_admin')  # Display `user_key` in the list view
    search_fields = ('email', 'username', 'user_key')  # Enable search by `user_key`
    list_filter = ('is_active', 'is_admin')
    readonly_fields = ('user_key',)  

admin.site.register(Account, AccountAdmin) 

from django.contrib import admin
from .models import Employee

# # Register your models here.
class Employees(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'cell', 'dept', 'emp_type', 'postal', 'ip_address', 'mac_address', 'reg_time', 'is_active', 'is_admin', 'password']
    
admin.site.register(Employee, Employees)
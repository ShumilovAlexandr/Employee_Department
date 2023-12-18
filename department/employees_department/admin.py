from django.contrib import admin

from .models import (Department,
                     Employee)


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['__all__']


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['__all__']


admin.site.register(Department)
admin.site.register(Employee)

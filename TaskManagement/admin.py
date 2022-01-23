from django.contrib import admin
from .models import Employee, Task, Project, Taskmanagment
from import_export.admin import ImportExportMixin

class EmployeeAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['user', 'Employee_id', 'Phone_number', 'date_joined']

class TaskAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['project', 'task_name', 'task_description']

class ProjectAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['name', 'description']

class TaskmanagmentAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['assignee', 'task_managment', 'status','priority', 'comment', 'start_date', 'end_date']

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Taskmanagment, TaskmanagmentAdmin)


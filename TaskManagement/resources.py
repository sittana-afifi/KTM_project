from import_export import resources
from .models import Employee, Task, Project, Taskmanagment
from import_export.widgets import ManyToManyWidget
from import_export.fields import Field
from import_export import resources,fields
from django.contrib.auth.models import User

class EmployeeResource(resources.ModelResource):

    def get_queryset(self):
        return Employee.objects.filter(user=self.user__username, Employee_id=self.Employee_id,Phone_number=self.Phone_number,date_joined=self.date_joined)
    class Meta:
        model = Employee
        fields = ('user__username', 'Employee_id','Phone_number','date_joined')
        export_order = ('user__username', 'Employee_id','Phone_number', 'date_joined')

class TaskResource(resources.ModelResource):

    def get_queryset(self):
        return Task.objects.filter(project=self.project, task_name=self.task_name,task_description=self.task_description)
    class Meta:
        model = Task
        fields = ('project__name', 'task_name','task_description',)
        export_order = ('project__name', 'task_name', 'task_description')

class ProjectResource(resources.ModelResource):

    def get_queryset(self):
        return Project.objects.filter(name=self.name, description=self.description)
    class Meta:
        model = Project
        fields = ('name', 'description',)
        export_order = ('name', 'description')

class TaskmanagmentResource(resources.ModelResource):

    def get_queryset(self):
        return Taskmanagment.objects.filter(assignee=self.assignee, assigneedTo=self.assigneedTo,task_managment=self.task_managment,status=self.status,priority=self.priority,comment=self.comment,
         start_date=self.start_date,end_date=self.end_date)
    class Meta:
        model = Taskmanagment
        fields = ('assignee__user__username','assigneedTo', 'task_managment__task_name', 'status','priority', 'comment', 'start_date', 'end_date',)
        export_order = ('assignee__user__username', 'assigneedTo', 'task_managment__task_name', 'status', 'priority','start_date','end_date','comment')
        widget=ManyToManyWidget(Employee, field='user')
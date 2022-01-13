import django_filters
from .models import *
from django import forms
from django_filters import FilterSet, ChoiceFilter
from flatpickr import DatePickerInput, TimePickerInput, DateTimePickerInput

class EmployeeFilter(django_filters.FilterSet):
    #user = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    #user = django_filters.CharFilter(lookup_expr=='icontains')
    class Meta:
        model = Employee
        fields = ['user', 'Employee_id','Phone_number','date_joined',]
        
class ProjectFilter(django_filters.FilterSet):
    name =django_filters.ModelChoiceFilter(queryset=Project.objects.all())
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Project
        fields = ['name',]

class TaskFilter(django_filters.FilterSet):
    project =django_filters.ModelChoiceFilter(queryset=Project.objects.all())
    task_name =django_filters.ModelChoiceFilter(queryset=Task.objects.all())
    task_name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Task
        fields = ['project', 'task_name', ]

class TaskmanagmentFilter(django_filters.FilterSet):
    task_managment = django_filters.ModelChoiceFilter(queryset=Task.objects.all())
    assignee = django_filters.ModelChoiceFilter(queryset=Employee.objects.all())
    assigneedTo = django_filters.ModelMultipleChoiceFilter(queryset=Employee.objects.all(),widget=forms.CheckboxSelectMultiple)
    TASK_STATUS = (
        ('TD', 'To do'),
        ('IP', 'In Progress'),
        ('C', 'Completed'),
    )
    TASK_PRIORITY = (
        ('H', 'High'),
        ('M', 'Meduim'),
        ('L', 'Low'),    
    )
    status = django_filters.ChoiceFilter(choices=TASK_STATUS)
    priority = django_filters.ChoiceFilter(choices=TASK_PRIORITY)

    class Meta:
        model = Taskmanagment
        fields = ['assignee', 'assigneedTo', 'task_managment', 'status', 'priority', 'start_date', 'end_date',]
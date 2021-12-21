from django import forms
from .models import Employee, Task, Taskmanagment
import datetime
from django.core.exceptions import ValidationError
from flatpickr import DatePickerInput, TimePickerInput, DateTimePickerInput

# Create Assign Task Form:
class AssignTaskForm(forms.ModelForm):
    class Meta:
        model = Taskmanagment
        fields = '__all__' 
    assignee = forms.ModelChoiceField(queryset = Employee.objects.all())
#   assigneedTo = forms.ModelChoiceField(queryset = Employee.objects.all())
    assigneedTo = forms.ModelMultipleChoiceField(queryset =Employee.objects.all())
    task_managment = forms.ModelChoiceField(queryset =Task.objects.all())
    TASK_STATUS = (
        ('TD', 'To do'),
        ('IP', 'In Progress'),
        ('C', 'Completed'),
    )
    status = forms.ChoiceField(choices=TASK_STATUS)
    TASK_PRIORITY = (
        ('H', 'High'),
        ('M', 'Meduim'),
        ('L', 'Low'),    
    )
    priority = forms.ChoiceField(choices=TASK_PRIORITY)
    comment = forms.CharField()
    start_date = forms.DateField(widget=DatePickerInput())
    end_date = forms.DateField(widget=DatePickerInput())

    def clean_assignee(self):
        data = self.cleaned_data['assignee']
        return data

    def clean_assigneedTo(self):
        data = self.cleaned_data['assigneedTo']
        return data

    def clean_status(self):
        data = self.cleaned_data['status']
        return data

    def clean_priority(self):
        data = self.cleaned_data['priority']
        return data

    def clean_assignee(self):
        data = self.cleaned_data['assignee']
        return data

    def clean_start_date(self):
        data = self.cleaned_data['start_date']
        
        if data < datetime.date.today():
            raise ValidationError(('Invalid date - Start Date cannot be in the past'))
        
        return data

    def clean_end_date(self):
        data = self.cleaned_data['end_date']
        return data
        
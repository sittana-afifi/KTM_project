from django import forms
from .models import Employee, Task, Taskmanagment
import datetime
from django.core.exceptions import ValidationError
from flatpickr import DatePickerInput, TimePickerInput, DateTimePickerInput

# -----------------------------------------------------------
# Assign Task to the Team Form  for Metting Room.
# display the attributes of form and ask user to enter all requirements to assign task.
# created by : Eman 
# creation date : -Dec-2021
# update date : -Dec-2022
# parameters : modelchoice , datefield input , multiple choices for team , charfiled 
# task creater , assignees of the task  , task name if it addhoc tasks or project name
# task status and the priority of it , start and end date of the task finally addtional comments.
# output: details of the assigned tasks request and the staus if it success or failed.
# -----------------------------------------------------------

class AssignTaskForm(forms.ModelForm):
    assignee = forms.ModelChoiceField(queryset = Employee.objects.all())
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
    comment = forms.CharField(required=False)
    start_date = forms.DateField(widget=DatePickerInput(options={"format": "mm/dd/yyyy","autoclose": True}))
    end_date = forms.DateField(widget=DatePickerInput(options={"format": "mm/dd/yyyy","autoclose": True}))
    
    class Meta:
        model = Taskmanagment
        fields = '__all__' 
    
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
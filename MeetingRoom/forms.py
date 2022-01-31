import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from TaskManagement.models import  Employee, Task, Project, Taskmanagment
from django.shortcuts import render
from flatpickr import DatePickerInput, TimePickerInput, DateTimePickerInput
from .models import ReservationMeetingRoom, Meeting

'''
-----------------------------------------------------------
Reservation Request Form  for Metting Room.
display the attributes of form.
and ask user to enter all requirements to reserve meeting room.
created by : Eman 
creation date : -Dec-2021
update date : -Dec-2022
parameters : modelchoice , datefield input , timefield , multiple choices for team
meeting room name, reservation date , the involved team in the meeting finally resrvation from and to time. 
output: details of the reservation request and the staus if it success or failed
-----------------------------------------------------------
'''

class ReservationForm(forms.ModelForm):
    meeting_room = forms.ModelChoiceField(queryset = Meeting.objects.all())
    reservation_date = forms.DateField(required=True, widget=DatePickerInput(options={"format": "mm/dd/yyyy","autoclose": True}))
    team = forms.ModelMultipleChoiceField(queryset =Employee.objects.all(),blank=True,required=False, widget=forms.CheckboxSelectMultiple) 
    reservation_from_time = forms.TimeField(widget=TimePickerInput(options={"format": "hh:mm","autoclose": True,"use24hours": True}))
    reservation_to_time = forms.TimeField(widget=TimePickerInput(options={"format": "hh:mm","autoclose": True}))
    meeting_project_name = forms.ModelChoiceField(queryset = Project.objects.all(), required=False)
    task_name = forms.ModelChoiceField(queryset = Task.objects.all(), required=False)

    class Meta:
        model = ReservationMeetingRoom
        fields = ['meeting_room', 'id','meeting_project_name', 'task_name' ,'reservation_date', 'reservation_from_time', 'reservation_to_time', 'team']
   
    def clean_reservation_from_time(self):
        data = self.cleaned_data['reservation_from_time']
        return data

    def clean_reservation_to_time(self):
        data = self.cleaned_data['reservation_to_time']
        return data

    def clean_meeting_room(self):
        data = self.cleaned_data['meeting_room']
        return data

    def clean_reservation_date(self):
        data = self.cleaned_data['reservation_date']
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - Date cannot be in the past'))
        return data

    def clean_team(self):
        data = self.cleaned_data['team']
        return data
    
    def clean_meeting_project_name(self):
        data = self.cleaned_data['meeting_project_name']
        return data

    def clean_task_name(self):
        data = self.cleaned_data['task_name']
        return data
   
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.meeting_room}'

    def get_absolute_url(self):
        """Returns the url to access a detail record for this project."""
        return reverse('reservationmeetingroom-detail', args=[str(self.id)])

'''
-----------------------------------------------------------
Update Reservation Request Form  for Metting Room.
display the attributes of form.
and ask user to enter all requirements to reserve meeting room.
created by : Eman 
creation date : -Dec-2021
update date : -Dec-2022
parameters : modelchoice , datefield input , timefield , multiple choices for team , charfiled 
meeting room name, reservation date , the involved team in the meeting finally resrvation from and to time. 
output: details of the reservation request and the staus if it success or failed , add meeting outcomes
also execlude the self reservation request from validation.
-----------------------------------------------------------
'''

class UpdateReservationForm(forms.ModelForm):
    meeting_room = forms.ModelChoiceField(queryset = Meeting.objects.all())
    reservation_date = forms.DateField(widget=DatePickerInput(options={"format": "mm/dd/yyyy","autoclose": True}), required=True )
    team = forms.ModelMultipleChoiceField(queryset =Employee.objects.all(),blank=True,required=False,widget=forms.CheckboxSelectMultiple) 
    reservation_from_time = forms.TimeField(widget=TimePickerInput(options={"format": "hh:mm","autoclose": True}))
    reservation_to_time = forms.TimeField(widget=TimePickerInput(options={"format": "hh:mm","autoclose": True}))
    meeting_project_name = forms.ModelChoiceField(queryset = Project.objects.all(), required=False)
    task_name = forms.ModelChoiceField(queryset = Task.objects.all(), required=False)
    meeting_outcomes = forms.CharField(max_length=1000, required=False, help_text='Enter the meeting outcomes', widget=forms.Textarea)
    
    class Meta:
        model = ReservationMeetingRoom
        fields = ['meeting_room', 'id','meeting_project_name','task_name', 'reservation_date', 'reservation_from_time', 'reservation_to_time', 'team', 'meeting_outcomes']
    
    def clean_reservation_from_time(self):
        data = self.cleaned_data['reservation_from_time']
        return data

    def clean_reservation_to_time(self):
        data = self.cleaned_data['reservation_to_time']
        return data

    def clean_meeting_room(self):
        data = self.cleaned_data['meeting_room']
        return data

    def clean_reservation_date(self):
        data = self.cleaned_data['reservation_date']
        return data

    def clean_team(self):
        data = self.cleaned_data['team']
        return data
    
    def clean_task_name(self):
        data = self.cleaned_data['task_name']
        return data

    def clean_meeting_project_name(self):
        data = self.cleaned_data['meeting_project_name']
        return data
    
    def clean_meeting_outcomes(self):
        data = self.cleaned_data['meeting_outcomes']
        return data

    def clean_validation(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)
        case_1 = ReservationMeetingRoom.objects.exclude(pk = self.pk).filter(meeting_room=self.meeting_room,reservation_date=self.reservation_date, reservation_from_time__gte= self.reservation_from_time, reservation_to_time= self.reservation_to_time).exists()
        case_2 = ReservationMeetingRoom.objects.exclude(pk = self.pk).filter(meeting_room=self.meeting_room,reservation_date=self.reservation_date, reservation_from_time__lte= self.reservation_from_time, reservation_to_time__gte= self.reservation_to_time).exists()
        case_3 = ReservationMeetingRoom.objects.exclude(pk = self.pk).filter(meeting_room=self.meeting_room,reservation_date=self.reservation_date, reservation_from_time__gte= self.reservation_from_time, reservation_to_time__lte=self.reservation_to_time).exists()
        case_4 = ReservationMeetingRoom.objects.exclude(pk = self.pk).filter(meeting_room=self.meeting_room,reservation_date=self.reservation_date, reservation_from_time__lte= self.reservation_from_time, reservation_to_time=self.reservation_to_time).exists()
        case_5 = ReservationMeetingRoom.objects.exclude(pk = self.pk).filter(meeting_room=self.meeting_room,reservation_date=self.reservation_date, reservation_from_time__gt=(self.reservation_from_time and self.reservation_to_time), reservation_to_time__lt=(self.reservation_to_time and self.reservation_from_time)).exists()
        case_6 = ReservationMeetingRoom.objects.exclude(pk = self.pk).filter(meeting_room=self.meeting_room,reservation_date=self.reservation_date, reservation_from_time__lt=(self.reservation_from_time and self.reservation_to_time), reservation_to_time__gt=(self.reservation_to_time and self.reservation_from_time)).exists()
        # if either of these is true, abort and render the error
        if case_1 or case_2 or case_3 or case_4 or case_5 or case_6 :
            raise ValidationError(('Selected Meeting room already reserved at this date and time ,please correct your information and then submit'))
            messages.error(request, "Selected Meeting room already reserved at this date and time ,please correct your information and then submit")
        return cleaned_data
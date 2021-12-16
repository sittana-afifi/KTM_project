import datetime
from django import forms
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from TaskManagement.models import  Employee, Task, Project, Taskmanagment
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from flatpickr import DatePickerInput, TimePickerInput, DateTimePickerInput
from .models import ReservationMeetingRoom, Meeting
from django.utils import timezone
from django.forms.utils import ErrorList


class ReservationForm(forms.ModelForm):
    class Meta:
        model = ReservationMeetingRoom
        fields = '__all__' 
        fields = ['meeting_room', 'id', 'reservation_date', 'reservation_from_time', 'reservation_to_time', 'team']
    meeting_room = forms.ModelChoiceField(queryset = Meeting.objects.all())
    reservation_date = forms.DateField(widget=DatePickerInput(options={"format": "mm/dd/yyyy","autoclose": True}))
    team = forms.ModelMultipleChoiceField(queryset =Employee.objects.all(),widget=forms.CheckboxSelectMultiple) 
    reservation_from_time = forms.TimeField()
    reservation_to_time = forms.TimeField()

    def clean_reservation_from_time(self):
        data = self.cleaned_data['reservation_from_time']
        # Check if the time is not in the past.   
        return data

    def clean_reservation_to_time(self):
        data = self.cleaned_data['reservation_to_time']
        # Check if the time is not in the past.
        return data

    def clean_meeting_room(self):
        data = self.cleaned_data['meeting_room']
        return data

    def clean_reservation_date(self):
        data = self.cleaned_data['reservation_date']
        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - Date cannot be in the past'))
        return data

    def clean_team(self):
        data = self.cleaned_data['team']
        return data
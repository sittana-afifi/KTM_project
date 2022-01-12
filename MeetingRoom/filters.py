import django_filters

from .models import *
from django import forms
from flatpickr import DatePickerInput, TimePickerInput, DateTimePickerInput

class ReservationMeetingRoomFilter(django_filters.FilterSet):
    team = django_filters.ModelMultipleChoiceFilter(queryset=Employee.objects.all(),
        widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = ReservationMeetingRoom
        fields = ['meeting_room', 'reservation_date', 'team', 'reservation_from_time', 'reservation_to_time',]

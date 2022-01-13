import django_filters
from .models import *
from django import forms
from django_filters import FilterSet, ChoiceFilter, BooleanFilter,DateFromToRangeFilter
from flatpickr import DatePickerInput, TimePickerInput, DateTimePickerInput

class ReservationMeetingRoomFilter(django_filters.FilterSet):
    team = django_filters.ModelMultipleChoiceFilter(queryset=Employee.objects.all(),
        widget=forms.CheckboxSelectMultiple)
    reservation_date = django_filters.DateFromToRangeFilter()
        
    class Meta:
        model = ReservationMeetingRoom
        fields = ['meeting_room', 'reservation_date', 'team', 'reservation_from_time', 'reservation_to_time',]

class MeetingRoomFilter(django_filters.FilterSet):
    name =django_filters.ModelChoiceFilter(queryset=Meeting.objects.all())
    name = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Meeting
        fields = ['name', 'description',]

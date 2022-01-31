import django_filters
from .models import *
from django import forms


class ReservationMeetingRoomFilter(django_filters.FilterSet):
    team = django_filters.ModelMultipleChoiceFilter(queryset=Employee.objects.all(),
        widget=forms.CheckboxSelectMultiple)
    reservation_date = django_filters.DateFromToRangeFilter(label='Reservation Date Range', widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'yyyy/mm/dd','class': 'datepicker', 'type': 'date'}))
        
    class Meta:
        model = ReservationMeetingRoom
        fields = ['meeting_room', 'reservation_date', 'team', 'reservation_from_time', 'reservation_to_time',]

class MeetingRoomFilter(django_filters.FilterSet):
    name =django_filters.ModelChoiceFilter(queryset=Meeting.objects.all())
    name = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Meeting
        fields = ['name', 'description',]

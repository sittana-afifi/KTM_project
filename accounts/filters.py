import django_filters
from django.contrib.auth.models import User
from .models import *
from django import forms
from django_filters import FilterSet, ChoiceFilter, BooleanFilter,DateFromToRangeFilter
from django_filters.widgets import BooleanWidget
from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput
from flatpickr import DatePickerInput, TimePickerInput, DateTimePickerInput

class CustomBooleanWidget(BooleanWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = (("", ("---")), ("true", ("Yes")), ("false", ("No")))

class AccountFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains')
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    is_staff = django_filters.BooleanFilter(widget=CustomBooleanWidget)
    is_superuser = django_filters.BooleanFilter(widget=CustomBooleanWidget)
    is_active = django_filters.BooleanFilter(widget=CustomBooleanWidget)
    date_joined = django_filters.DateFromToRangeFilter(label='Date Joined Range', widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'yyyy/mm/dd','class': 'datepicker', 'type': 'date'}))

    class Meta:
        model = User
        fields = ['username', 'date_joined','first_name', 'last_name','is_staff','is_superuser','is_active',]

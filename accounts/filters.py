import django_filters
from django.contrib.auth.models import User
from .models import *
from django import forms
from django_filters import FilterSet, ChoiceFilter, BooleanFilter,DateFromToRangeFilter
from flatpickr import DatePickerInput, TimePickerInput, DateTimePickerInput

class AccountFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains')
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    is_staff = django_filters.BooleanFilter()
    is_superuser = django_filters.BooleanFilter()
    is_active = django_filters.BooleanFilter()
    date_joined = django_filters.DateFromToRangeFilter()
    date_joined_end = django_filters.DateFromToRangeFilter()

    class Meta:
        model = User
        fields = ['username', 'date_joined','first_name', 'last_name','is_staff','is_superuser','is_active',]

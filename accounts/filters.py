import django_filters
from django.contrib.auth.models import User
from .models import *
from django import forms
from django_filters import FilterSet, ChoiceFilter, BooleanFilter
from flatpickr import DatePickerInput, TimePickerInput, DateTimePickerInput

class AccountFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains')
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    is_staff = BooleanFilter()
    is_superuser = BooleanFilter()
    is_active = BooleanFilter()
    class Meta:
        model = User
        fields = ['username', 'date_joined','first_name', 'last_name','is_staff','is_superuser','is_active',]

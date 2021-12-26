
from django import forms
from django import forms
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.forms.fields import BooleanField
from django.shortcuts import  render
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from accounts.models import Account
from flatpickr import DatePickerInput , DateTimePickerInput





class UserForm(forms.ModelForm):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    class Meta:
            model = User
            fields = ('username' , )
    def clean_username(self):
            if self.is_valid():
                username = self.cleaned_data['username']
            try:
                account= User.objects.exclude(pk=self.instance.pk).get(username=username)
            except User.DoesNotExist:
                return username
            raise forms.ValidationError('username "%s%" is already in use.'% username)



class AccountCreateForm(forms.ModelForm):
    email = forms.EmailField(label='Email', min_length=4, max_length=150)
    first_name = forms.CharField(label='First Name', min_length=4, max_length=150)
    last_name = forms.CharField(label='Last Name', min_length=4, max_length=150)
    username = forms.CharField(label='User Name', min_length=4, max_length=150)
    #last_login = forms.DateField(widget=DateTimePickerInput(options={"format": "mm/dd/yyyy","autoclose": True}),required=True)
    #is_active= forms.BooleanField(label="Active", required= False, initial=False)
    #is_staff= forms.BooleanField(label="Staff status" , required= False, initial=False)
    #is_superuser= forms.BooleanField(label="Superuser status" , required= False ,initial=False)

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email')#, 'is_superuser', 'is_active', 'is_staff')
        #'last_login',
    
        def clean_username(self):
            print("entered is valid")
            username = self.cleaned_data['username'].lower()
            r = User.objects.filter(username=username)
            if r.count():
                raise  ValidationError("Username already exists")
            return username

        def clean_email(self):
            print("entered is valid")
            email = self.cleaned_data['email'].lower()
            r = User.objects.filter(email=email)
            if r.count():
                raise  ValidationError("Email already exists")
            return email

        def clean_first_name(self):
            print("entered is valid")
            first_name = self.cleaned_data['first_name'].lower()
            r = User.objects.filter(first_name=first_name)
            if r.count():
                raise  ValidationError("first_name already exists")
            return first_name

        def clean_last_name(self):
            print("entered is valid")
            last_name = self.cleaned_data['last_name'].lower()
            r = User.objects.filter(last_name=last_name)
            if r.count():
                raise  ValidationError("last_name already exists")
            return last_name
            
'''
        def clean(self):
                if self.is_valid():
                    #first_name = self.cleaned_data['first_name']
                    last_name = self.cleaned_data['last_name']
                    #email = self.cleaned_data['email']
                    #username = self.cleaned_data['username']
                    #last_login = self.cleaned_data['last_login']
                    is_active = self.cleaned_data['is_active']
                    is_staff = self.cleaned_data['is_staff']
                    is_superuser = self.cleaned_data['is_superuser']

    ''' 
    
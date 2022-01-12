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
            print ('enter validation username')
            username = self.cleaned_data['username'].lower()  
            new = User.objects.filter(username = username)  
            if new.count():  
                raise ValidationError("User Already Exist")  
            return username  

class AccountCreateForm(forms.ModelForm):
    email = forms.EmailField( widget=forms.TextInput(attrs={'readonly':'readonly'}),label='Email', min_length=4, max_length=150)
    first_name = forms.CharField( widget=forms.TextInput(attrs={'readonly':'readonly'}),label='First Name', min_length=4, max_length=150)
    last_name = forms.CharField( widget=forms.TextInput(attrs={'readonly':'readonly'}),label='Last Name', min_length=4, max_length=150)
    username = forms.CharField( widget=forms.TextInput(attrs={'readonly':'readonly'}),label='User Name', min_length=4, max_length=150)    
    class Meta:
        model = User
        exclude  = ('password','last_login','is_superuser', 'is_active', 'is_staff','date_joined',)    

        def clean_username(self):
                print("entered is valid")

                if self.is_valid():
                    username = self.cleaned_data['username']
                try:
                    account= User.objects.exclude(pk=self.instance.pk).get(username=username)
                except User.DoesNotExist:
                    return username
                raise forms.ValidationError('username "%s%" is already in use.'% username)

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
            
        def clean(self):
                if self.is_valid():
                    is_active = self.cleaned_data['is_active']
                    is_staff = self.cleaned_data['is_staff']
                    is_superuser = self.cleaned_data['is_superuser']
from django import forms
from django.contrib.auth.models import User
from django.shortcuts import  render
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import os, logging, logging.config # Logging view in Django.

# Create a logger for this file or the name of the log level or Get an instance of a logger
logger = logging.getLogger(__name__)
logger = logging.getLogger(__file__)

"""
    A class used to represent an Account
    ...

    Attributes
    ----------
    username : CharField
        the name of the user

    Methods
    -------
    clean_username(self)
        Prints the animals name and what sound it makes

    created by :
    -------
        Sittana 

    creation date : 
    -------
        01-Dec-2021

    update date :
    -------
         21-Jan-2022
"""

class UserForm(forms.ModelForm):
    logger.info('enter UserForm form.')
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    class Meta:
            model = User
            fields = ('username' , )
    def clean_username(self):
            logger.info('enter clean_username function in UserForm.')
            """
            Parameters
            ----------
            self : 
                 self.instance is your current user

            return:
            ----------
              a dictionary of validated form input fields and their values

            Raises
            ------
            ValidationError
                If the user is already exist in the Database.
            """

            username = self.cleaned_data['username'].lower()  
            new = User.objects.filter(username = username)  
            if new.count():  
                logger.info('raise ValidationError (User Already Exist).')
                raise ValidationError("User Already Exist")  
            return username  

"""
    A class used to create an Account
    ...

    Attributes
    ----------
    email : EmailField
        the email of the user
    first_name : CharField
        the first name of the user
    last_name : CharField
        the last name of the user
    username : CharField
        the name of the user

    Methods
    -------
    clean_username(self)
        validate the username
    clean_email(self)
        validate the user email
    clean_first_name(self)
        validate the user's first anme
    clean_last_name(self)
        validate the user's last anme

    created by :
    -------
        Sittana Afifi

    creation date : 
    -------
        01-Dec-2021

    update date :
    -------
         21-Jan-2022
"""
class AccountCreateForm(forms.ModelForm):
    email = forms.EmailField( widget=forms.TextInput(attrs={'readonly':'readonly'}),label='Email', min_length=4, max_length=150)
    first_name = forms.CharField( widget=forms.TextInput(attrs={'readonly':'readonly'}),label='First Name', min_length=4, max_length=150)
    last_name = forms.CharField( widget=forms.TextInput(attrs={'readonly':'readonly'}),label='Last Name', min_length=4, max_length=150)
    username = forms.CharField( widget=forms.TextInput(attrs={'readonly':'readonly'}),label='User Name', min_length=4, max_length=150)    
    class Meta:
        model = User
        exclude  = ('password','last_login','is_superuser', 'is_active', 'is_staff','date_joined',)    

        def clean_username(self):
                """
                Parameters
                ----------
                self : 
                    self.instance is your current user
                    
                return:
                ----------
                    a dictionary of validated username field and it's value
                
                Raises
                ------
                ValidationError
                    If the username is already exist in the Database.
                """
                logger.info('entered is clean_username in AccountCreateForm.')
                if self.is_valid():
                    logger.info('clean_username is valid.')
                    username = self.cleaned_data['username']
                try:
                    account= User.objects.exclude(pk=self.instance.pk).get(username=username)
                except User.DoesNotExist:
                    return username
                raise forms.ValidationError('username "%s%" is already in use.'% username)

        def clean_email(self):
            """
            Parameters
            ----------
            self : 
                 self.instance is your current user

            return:
            ----------
              a dictionary of validated email field and it's value

            Raises
            ------
            ValidationError
                    If the email is already exist in the Database.
            """
            logger.info('entered is clean_email in AccountCreateForm.')
            email = self.cleaned_data['email'].lower()
            r = User.objects.filter(email=email)
            if r.count():
                raise  ValidationError("Email already exists")
            return email

        def clean_first_name(self):
            """
            Parameters
            ----------
            self : 
                 self.instance is your current user

            return:
            ----------
                a dictionary of validated first_name field and it's value

            Raises
            ------
            ValidationError
                    If the first_name is already exist in the Database.
            """
            logger.info('entered is clean_first_name in AccountCreateForm.')
            first_name = self.cleaned_data['first_name'].lower()
            r = User.objects.filter(first_name=first_name)
            if r.count():
                raise  ValidationError("first_name already exists")
            return first_name

        def clean_last_name(self):
            """
            Parameters
            ----------
            self : 
                 self.instance is your current user

            return:
            ----------
                a dictionary of validated last_name field and it's value
            
            Raises
            ------
            ValidationError
                    If the last_name is already exist in the Database.
            """
            logger.info('entered is clean_last_name in AccountCreateForm.')
            last_name = self.cleaned_data['last_name'].lower()
            r = User.objects.filter(last_name=last_name)
            if r.count():
                raise  ValidationError("last_name already exists")
            return last_name
            
        
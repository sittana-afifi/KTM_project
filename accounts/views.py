from urllib import request
from django.db import connection
from django.db.models import fields
from django.forms import formsets
from django.forms.forms import Form
from django.forms.widgets import FILE_INPUT_CONTRADICTION
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls.base import is_valid_path, reverse
from django.views import generic
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView , DeleteView , CreateView 
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from accounts.models import Account
from django_auth_ldap.backend import LDAPBackend
from .forms import  UserForm , AccountCreateForm 
from django.shortcuts import render
from django.contrib.auth import authenticate as authenticate_django
from pathlib import Path
from django.contrib import messages




# Logging view in Django:
# First import the logging library from Python's standard library:
import os 
import logging
from django.http import HttpResponse
# Create a logger for this file or the name of the log level:
# or Get an instance of a logger:
logger = logging.getLogger(__name__)
import logging.config
logger = logging.getLogger(__file__)
from django.utils.log import DEFAULT_LOGGING


@login_required
def index(request):
    """View function for home page of site."""
    logger.info("enter index function.")
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    context = {
        'num_visits':num_visits,
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
    logger.info("enter index function.")





# Add new user.

def getUserInfoFromLDAP(request):
    '''Get User Info from LDAP'''
    username = request.POST.get('username')
    try:
        user = LDAPBackend().populate_user(username)
        if user is None:
            
            raise Exception("User Already Exit")
        user.delete()
    except AttributeError as e:
        print("Error")
    # dictionary for initial data with 
    # field names as keys
    init = {
        'username' : user.username,
        'first_name' : user.first_name,
        'last_name' : user.last_name,
        'email' :  user.email,

        }
    # add the dictionary during initialization    
    u_form = AccountCreateForm( initial = init)
    return u_form

def submitUserForm(request):
    u_form = AccountCreateForm( request.POST)  
    if u_form.is_valid() :
        u_form.save()
        return redirect( 'user_list') 
    #return render(request, 'usersubmitform.html')

def createUser(request):
    context = {}
    if request.method == 'GET' :
        u_form = UserForm()
        context ['u_form' ]= u_form
        return render(request, 'get_user_info.html', context) 
    if request.method == 'POST' :
        username = request.POST.get('username')

        isExist = User.objects.filter(username = username).exists()
        if isExist:
                messages.error(request, 'User Already Exist')
                return redirect( 'get_user_info') 
        
        try:
            u_form = getUserInfoFromLDAP(request) 
            return render(request, 'user_create.html', {'u_form' :u_form}) 

        except Exception as e:
            messages.error(request, 'User Doesn\'t exist in Active Directory')
            u_form = UserForm()
            return render(request, 'get_user_info.html', {'u_form' :u_form}) 


# view the list of the users.

class usersListView(LoginRequiredMixin,generic.ListView):
    logger.info("enter index function.")
    model = User
    template_name ='accounts/user_list.html'



# view details of the specific user.
class UserDetailView(LoginRequiredMixin,generic.DetailView):
    model = User
    template_name ='accounts/user_detail.html'



# update specific user with specific fields.
class UserUpdate(LoginRequiredMixin,UpdateView):
    
    model = User
    #exclude  = ('password','last_login','is_superuser', 'is_active','date_joined', )
    form_class = AccountCreateForm
    #fields = ['username','first_name','last_name','email',]




# delete specific user.
class UserDelete(LoginRequiredMixin,DeleteView):
    model = User
    success_url = reverse_lazy('user_list')



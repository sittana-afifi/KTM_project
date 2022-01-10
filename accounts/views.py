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
import os, logging, logging.config # Logging view in Django:
from django.http import HttpResponse
logger = logging.getLogger(__name__) # Create a logger for this file or the name of the log level or Get an instance of a logger
logger = logging.getLogger(__file__)


@login_required
def index(request):
    """View function for home page of site."""
    logger.info('info This logs an info message.')
    logger.debug(' debug This logs an info message.')
    logger.error(' error This logs an info message.')
    logger.warning('warning This logs an info message.')
    logger.critical('critical This logs an info message.')
    logger.info("This logs an info message.")
    logger.error("enter index function.")
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    context = {
        'num_visits':num_visits,
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)





# Add new user.

def getUserInfoFromLDAP(request):
    '''Get User Info from LDAP'''
    logger.info("enter getUserInfoFromLDAP function.")

    username = request.POST.get('username')
    try:
        logger.info("enter TRY inside getUserInfoFromLDAP function.")

    
        user = LDAPBackend().populate_user(username)
        if user is None:
            logger.info("User fron ldap is None.")
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
    logger.info("enter submitUserForm function.")

    u_form = AccountCreateForm( request.POST)  
    if u_form.is_valid() :
        logger.info("u_form is  Valid.")
        u_form.save()
        return redirect( 'user_list') 
    #return render(request, 'usersubmitform.html')

def createUser(request):
    logger.info("enter createUser function.")

    context = {}
    if request.method == 'GET' :
        logger.info("The Request is GET.")
        u_form = UserForm()
        context ['u_form' ]= u_form
        return render(request, 'get_user_info.html', context) 
    if request.method == 'POST' :
        logger.info("The Request is POST.")
        username = request.POST.get('username')
        isExist = User.objects.filter(username = username).exists()
        if isExist:
                logger.info("Enter isExist.")
                messages.error(request, 'User Already Exist')
                return redirect( 'get_user_info') 
        
        try:
            logger.info("Enter TRY.")
            u_form = getUserInfoFromLDAP(request) 
            return render(request, 'user_create.html', {'u_form' :u_form}) 

        except Exception as e:
            logger.info("Enter Exception.")
            messages.error(request, 'User Doesn\'t exist in Active Directory')
            u_form = UserForm()
            return render(request, 'get_user_info.html', {'u_form' :u_form}) 


# view the list of the users.

class usersListView(LoginRequiredMixin,generic.ListView):
    logger.info("Enter usersListView.")
    model = User
    template_name ='accounts/user_list.html'



# view details of the specific user.
class UserDetailView(LoginRequiredMixin,generic.DetailView):
    logger.info("Enter UserDetailView.")
    model = User
    template_name ='accounts/user_detail.html'



# update specific user with specific fields.
class UserUpdate(LoginRequiredMixin,UpdateView):
    logger.info("Enter UserUpdate.")
    model = User
    #exclude  = ('password','last_login','is_superuser', 'is_active','date_joined', )
    form_class = AccountCreateForm
    #fields = ['username','first_name','last_name','email',]




# delete specific user.
class UserDelete(LoginRequiredMixin,DeleteView):
    logger.info("Enter UserDelete.")
    model = User
    success_url = reverse_lazy('user_list')



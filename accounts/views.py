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
from django.contrib.auth import authenticate as authenticate_django
from pathlib import Path
from django.contrib import messages
from .filters import AccountFilter
import datetime
import csv
from django.http import HttpResponse
from django.contrib.auth.models import User
import os, logging, logging.config # Logging view in Django.
import xlwt
from .resources import AccountResource
from tablib import Dataset

# Create a logger for this file or the name of the log level or Get an instance of a logger
logger = logging.getLogger(__name__)
logger = logging.getLogger(__file__)

# -----------------------------------------------------------
# View function for home page of site.
# display the Number of times visited this page.
# and contians details about the web application and how to use it.
# created by : Eman 
# creation date : 20-Dec-2021
# update date : 10-Jan-2022
# parameters : Number (integer)
# output: Number Integer + static conent
# -----------------------------------------------------------

@login_required
def index(request):
    """View function for home page of site."""
    logger.info('info This logs an info message.')
    logger.debug(' debug This logs an info message.')
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    context = {
        'num_visits':num_visits,
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

# Add new user.
def getUserInfoFromLDAP(request):
    #Get User Info from LDAP
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
        return redirect( 'user-filter') 

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
    filter_class = AccountFilter

# UserFilter View:    
def AccountViewFilter(request):
    userf_list = User.objects.all()
    userf_filter = AccountFilter(request.GET, queryset= userf_list)
    return render(request, 'accounts/user_list.html', {'filter': userf_filter})

# view details of the specific user.
class UserDetailView(LoginRequiredMixin,generic.DetailView):
    logger.info("Enter UserDetailView.")
    model = User
    template_name ='accounts/user_detail.html'

# update specific user with specific fields.
class UserUpdate(LoginRequiredMixin,UpdateView):
    logger.info("Enter UserUpdate.")
    model = User
    form_class = AccountCreateForm

# delete specific user.
class UserDelete(LoginRequiredMixin,DeleteView):
    logger.info("Enter UserDelete.")
    model = User
    success_url = reverse_lazy('user-filter')

import _datetime
today = _datetime.date.today()
i = 10
def export_users_xls(request):
    userf_filter = AccountFilter(request.GET, queryset=User.objects.all())
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename={date}-Users-.xls'.format(date=today.strftime('%Y-%m-%d'),)
    
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    date_style = xlwt.easyxf(num_format_str='DD/MM/YYYY')
    time_style = xlwt.easyxf(num_format_str='HH:MM AM/PM') 

    columns = ['Username', 'First name', 'Last name', 'Email address', 'Is_SuperUser', 'Is_Active', 'Is_Staff','Date_Joined']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    dataset = AccountResource().export(userf_filter.qs)
    for row in dataset:
        row_num += 1
        for col_num in range(len(row)):
            if isinstance(row[col_num], datetime.date):
                ws.write(row_num, col_num, row[col_num], date_style)
            elif isinstance(row[col_num], datetime.time):
                ws.write(row_num, col_num, row[col_num], time_style)
            else:
                ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response
from typing_extensions import Self
from urllib import request
from django.db import connection
from django.forms import formsets
from django.forms.forms import Form
from django.forms.widgets import FILE_INPUT_CONTRADICTION
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls.base import is_valid_path, reverse
from django.views import generic
import datetime
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView , DeleteView , CreateView 
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required



@login_required
def index(request):
    """View function for home page of site."""
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    context = {
        'num_visits':num_visits,
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
from django_auth_ldap.backend import LDAPBackend
from .forms import UserForm , AccountCreateForm 
from django.shortcuts import render
from ldap3 import Server, Connection, ALL
from django.contrib.auth import authenticate as authenticate_django
from pathlib import Path
import ldap



from django.contrib.auth import get_backends, get_user_model
from django.contrib.auth.backends import ModelBackend 

    


'''
def authenticate( request):
    # 1-get if the user is in the database or not
    # 2-if the number is in the active directory or not
    #ldap=load_properties("LDAP")
    #url =decrypt(ldap['url'])
    connect = ldap.initialize('ldap://192.168.1.11')
    connect.set_option(ldap.OPT_REFERRALS, 0)
    connect.simple_bind_s('Abc123++')

    result = connect.search_s('dc=BD,dc=com',
                          ldap.SCOPE_SUBTREE,
                          'cn=bind',)
    
    url='ldap://192.168.1.11'
    server = Server(url)
    ldap_conn = Connection(server, user=username , password=password)    
    user=authenticate_django(request, email= username,password= password)
    return user 
    
    return result

print(authenticate(request),';;;;;;;;;;;')
'''


# Add new user.
'''
def moiz(request):
    if request.POST:
        u_form = AccountCreateForm(request.POST)
        if u_form.is_valid():
            u_form.save()
        return render(request, 'user_create1.html')  
    u_form=AccountCreateForm()
    context = { 'u_form':u_form } 
    return render(request, 'user_create1.html',context)  
'''



from django_auth_ldap import backend
def getUserInfoFromLDAP(request):
    '''Get User Info from LDAP'''
    context = {}
    username = request.POST.get('username')
    #print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
    #u = User.objects.filter(username=username)
    #print(u) 
    user1 = backend.LDAPBackend().populate_user(username)
    
    # Create user and save to the database
    #user = User.objects.create_user(username, user1.email, user1.password)
    # Update fields and then save again
    #user.first_name = user1.first_name
    #user.last_name = user1.last_name
    #user1.delete()
    #user.save()
    
    #u = User.objects.filter(username=username)
    #print(u,';;;;;;;;;;;;;')
    if user1 is None:
        raise Exception("No user named ",username) 
    # dictionary for initial data with 
    # field names as keys
    init = {
        'username' : user1.username,
        'first_name' : user1.first_name,
        'last_name' : user1.last_name,
        'email' :  user1.email,
        #'is_active' : 'True',
        #'is_staff':'True',
        #'is_superuser':'True',
        }
    # add the dictionary during initialization
    u_form = AccountCreateForm(initial = init)
    context ['u_form' ]= u_form
    return u_form

def createUser(request):
    context = {}
    if request.method == 'GET' :
        u_form = UserForm()
        context ['u_form' ]= u_form
        return render(request, 'get_user_info.html', context) 
    if request.method == 'POST' :
        u_form = getUserInfoFromLDAP(request)     
        #print(u_form)
        context ['u_form' ]= u_form
        return render(request, 'user_create.html', context) 


  
'''
def UserCreateForm(request):
    print('3',request.method)
    context ={}
    if request.method == 'POST':
        u_form = AccountCreateForm( request.POST)    
        #context['u_form']= u_form
        print(u_form)
        print(u_form.is_valid())
        if u_form.is_valid():
            u_form.save()
        #return render (request , 'user_create1.html')
    elif request.method == 'GET':

        u_form = AccountCreateForm(request.POST)
    context['u_form']= u_form

    return render(request, 'user_create1.html', context) #later forward to user-list
'''
     
# view the list of the users.

class usersListView(LoginRequiredMixin,generic.ListView):
    model = User
    template_name ='accounts/user_list.html'



# view details of the specific user.
class UserDetailView(LoginRequiredMixin,generic.DetailView):
    model = User
    template_name ='accounts/user_detail.html'



# update specific user with specific fields.
class UserUpdate(LoginRequiredMixin,UpdateView):
    model = User
    fields =['is_active','is_staff','is_superuser','groups','user_permissions']
    success_url = reverse_lazy('user_list')



# delete specific user.
class UserDelete(LoginRequiredMixin,DeleteView):
    model = User
    success_url = reverse_lazy('user_list')



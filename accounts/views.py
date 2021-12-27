from django.views import generic
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView , DeleteView , CreateView 
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django_auth_ldap.backend import LDAPBackend
from .forms import UserForm , AccountCreateForm 
from django.shortcuts import render
from django.contrib.auth import authenticate as authenticate_django
from pathlib import Path






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




# Add new user.

def getUserInfoFromLDAP(request):
    '''Get User Info from LDAP'''
    username = request.POST.get('username')
    user1 = LDAPBackend().populate_user(username)
    if user1 is None:
        raise Exception("No user named ", username)
    user1.delete()
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
    u_form = AccountCreateForm( initial = init)
    return u_form

def submitUserForm(request):
    u_form = AccountCreateForm( request.POST)  
    if(u_form.is_valid()):
        u_form.save()
    return render(request, 'usersubmitform.html')
    
def createUser(request):
    context = {}
    if request.method == 'GET' :
        u_form = UserForm()
        context ['u_form' ]= u_form
        return render(request, 'get_user_info.html', context) 
    if request.method == 'POST' :
        u_form = getUserInfoFromLDAP(request)    
        context ['u_form' ]= u_form
        return render(request, 'user_create.html', {'u_form' :u_form}) 


  

     
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



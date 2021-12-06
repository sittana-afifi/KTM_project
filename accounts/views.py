from django.views import generic
import datetime
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView , DeleteView , CreateView 
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User



# view the list of the users.

class usersListView(PermissionRequiredMixin,generic.ListView):

    permission_required = 'catalog.can_mark_returned'
    model = User
    template_name ='accounts/user_list.html'



# view details of the specific user.
class UserDetailView(generic.DetailView):
    model = User
    template_name ='accounts/user_detail.html'



# update specific user with specific fields.
class UserUpdate(UpdateView):
    model = User
    fields =['is_active','is_staff','is_superuser','groups','user_permissions']
    success_url = reverse_lazy('user_list')



# delete specific user.
class UserDelete(DeleteView):
    model = User
    success_url = reverse_lazy('user_list')


# Add new user.

class UserCreate(CreateView):
    model = User
    fields =['username','first_name','last_name','password','email','is_active','is_staff','is_superuser','groups','user_permissions','last_login','date_joined']
    initial = {'is_superuser': 'False' ,'date_joined':str(datetime.date.today()), 'last_login':str(datetime.date.today()) }
    success_url = reverse_lazy('users')






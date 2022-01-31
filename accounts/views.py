from django.views import generic
from django.contrib.auth.mixins import  LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView , DeleteView  
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django_auth_ldap.backend import LDAPBackend
from .forms import  UserForm , AccountCreateForm 
from django.contrib import messages
from .filters import AccountFilter
import _datetime, csv
from django.http import HttpResponse
import logging, logging.config # Logging view in Django.
import xlwt
import  logging, logging.config # Logging view in Django.
import xlwt, csv # use in export function
from .resources import AccountResource

# Create a logger for this file or the name of the log level or Get an instance of a logger
logger = logging.getLogger(__name__)
logger = logging.getLogger(__file__)

@login_required
def index(request):
    """View function for home page of site display the Number of times visited this page.

    Parameters
    ----------
    name : str
        The name of the file
    returns : int, str 
        The Number of times visited this page and the how page static information
    """
    
    logger.info('info This logs an info message.')
    logger.debug(' debug This logs an info message.')

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    context = {
        'num_visits':num_visits,
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

def getUserInfoFromLDAP(request):
    """ use to get user information from LDAP
    created by :
    -------
        Sittana Afifi

    creation date : 
    -------
        01-Dec-2021

    update date :
    -------
         21-Jan-2022

    Parameters
    ----------
    request : 
        uses to pass state through the system

    return:
    ----------
        A form contained user data from imported from LDAP

    Raises
    ------
    Exception
        If the user is already exist in the Database.
    """
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
    # dictionary for initial data with field names as keys
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
    """ validate AccountCreateForm and save it.
    created by :
    -------
        Sittana Afifi

    creation date : 
    -------
        01-Dec-2021

    update date :
    -------
         21-Jan-2022

    Parameters
    ----------
    request : 
        uses to pass state through the system

    return:
    ----------
        Return an HttpResponseRedirect to 'user-filter' URL for the arguments passed.

    """
    logger.info("enter submitUserForm function.")
    u_form = AccountCreateForm( request.POST)  
    if u_form.is_valid() :
        logger.info("u_form is Valid.")
        u_form.save()
        return redirect( 'user-filter') 

def createUser(request):
    """ post UserForm content and get username as input.
    created by :
    -------
        Sittana Afifi

    creation date : 
    -------
        01-Dec-2021

    update date :
    -------
         21-Jan-2022

    Parameters
    ----------
    request : 
        uses to pass state through the system

    return:
    ----------
        Return an HttpResponseRedirect to 'get_user_info' URL for the arguments passed.
    """
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
            
"""
    A class used to view user list
    ...

    Attributes
    ----------
    model : 
        User
    template_name :
        'accounts/user_list.html'

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
class usersListView(LoginRequiredMixin,generic.ListView):
    logger.info("Enter usersListView.")
    model = User
    template_name ='accounts/user_list.html'
    filter_class = AccountFilter
    
def AccountViewFilter(request):
    """ filter user list view.
    created by :
    -------
        Eman

    creation date : 
    -------
        18-Dec-2021

    update date :
    -------
         21-Jan-2022

    Parameters
    ----------
    request : 
        uses to pass state through the system

    return:
    ----------
        Return an HttpResponseRedirect to 'accounts/user_list.html' for the arguments passed.
    """
    userf_list = User.objects.all()
    userf_filter = AccountFilter(request.GET, queryset= userf_list)
    return render(request, 'accounts/user_list.html', {'filter': userf_filter})

"""
    A class used to view user detail.
    ...

    Attributes
    ----------
    model : 
        User
    template_name :
        'accounts/user_detail.html'

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
class UserDetailView(LoginRequiredMixin,generic.DetailView):
    logger.info("Enter UserDetailView.")
    model = User
    template_name ='accounts/user_detail.html'

""" 
    update user's information.
    ...

    Attributes
    ----------
    model : 
        User
    form_class :
        AccountCreateForm

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
class UserUpdate(LoginRequiredMixin,UpdateView):
    logger.info("Enter UserUpdate.")
    model = User
    form_class = AccountCreateForm

""" 
    delete specific user.
    ...

    Attributes
    ----------
    model : 
        User

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
class UserDelete(LoginRequiredMixin,DeleteView):
    logger.info("Enter UserDelete.")
    model = User
    success_url = reverse_lazy('user-filter')

today = _datetime.date.today()
"""
    A function used to export model information from database.
    ...

    Attributes
    ----------
    list : list
        the list of the user
        first choose filter option from filter 
        function and then export file

    Methods
    -------
        import-export method in django

    output 
    -------
    file with different format (csv, excel ,yaml)

    -------
    created by :
    -------
        Eman 

    creation date : 
    -------
        15-Jan-2021

    update date :
    -------
        20-Jan-2022
"""

@login_required
def export_users_xls(request):

    """ Export all user list details view from database and allow filter option
        with different firmat(excel , json , yaml) .

        If there is no filter option choosed all users in database will be export.

        Parameters
        ----------
        file format : (excel , json , yaml) 
            choose the file format from dropdown list

        Result
        ------
        export requested data with requested format.
        """

    logger.info("Export Function.")
    file_format = request.POST['file-format']
    userf_filter = AccountFilter(request.GET, queryset=User.objects.all())
    dataset = AccountResource().export(userf_filter.qs)

    if file_format == 'CSV':
        logger.info("Export csv file.")
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={date}-Users.csv'.format(date=today.strftime('%Y-%m-%d'),)
        writer = csv.writer(response)
        writer.writerow(['Username', 'First name', 'Last name', 'Email address', 'Is_SuperUser', 'Is_Active', 'Is_Staff','Date_Joined'])
        for std in dataset:
            writer.writerow(std)
        return response 

    elif file_format == 'JSON':
        logger.info("export json file.")
        response = HttpResponse(dataset.json, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename={date}-Users.json'.format(date=today.strftime('%Y-%m-%d'),)
        return response

    elif file_format == 'YAML':
        logger.info("Export yaml file.")
        response = HttpResponse(dataset.yaml,content_type='application/x-yaml')
        response['Content-Disposition'] = 'attachment; filename={date}-Users.yaml'.format(date=today.strftime('%Y-%m-%d'),)
        return response

    elif file_format == 'Excel':
        logger.info("Export excel file.")
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename={date}-Users.xls'.format(date=today.strftime('%Y-%m-%d'),)
    
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Users')

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['Username', 'First name', 'Last name', 'Email address', 'Is_SuperUser', 'Is_Active', 'Is_Staff','Date_Joined']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()
        for row in dataset:
            row_num += 1
            for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response

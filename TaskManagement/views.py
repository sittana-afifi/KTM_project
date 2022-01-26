from django.contrib.auth.mixins import  LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic
from .models import Employee , Taskmanagment, Project, Task
from django.views.generic.edit import UpdateView , DeleteView , CreateView 
from django.contrib.auth.decorators import login_required, permission_required
from .forms import AssignTaskForm
import csv
from django import forms
from .forms import AssignTaskForm, UpdateAssignTaskForm
import datetime, _datetime
import csv, xlwt # use in export functions
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput
from flatpickr import DatePickerInput, TimePickerInput, DateTimePickerInput
from flatpickr.utils import GenericViewWidgetMixin
import os, logging, logging.config # Logging view in Django.
from TaskManagement.filters import EmployeeFilter, ProjectFilter, TaskFilter, TaskmanagmentFilter
from .resources import EmployeeResource, TaskResource, ProjectResource, TaskmanagmentResource
import _datetime
from tablib import Dataset 
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User

# Create a logger for this file or the name of the log level or Get an instance of a logger
logger = logging.getLogger(__name__) 
logger = logging.getLogger(__file__)

"""
    A class used to view a list of all employees.
    ...

    Attributes
    ----------
    model : 
        Employee
    template_name :
        'TaskManagement/employee_list.html'
    filter_class : 
        EmployeeFilter

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
class EmployeesListView(LoginRequiredMixin,generic.ListView):
    logger.info("Enter EmployeesListView.")
    model = Employee
    template_name ='TaskManagement/employee_list.html'
    paginate_by = 5
    filter_class = EmployeeFilter

def EmployeeViewFilter(request):
    """ Employee Filter View.
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
            Return an HttpResponseRedirect to 'TaskManagement/employee_list.html' for the arguments passed.
        """
@login_required    
def EmployeeViewFilter(request):
    """Employee View filter for employee list and show filter options.

    Parameters
    ----------
    name : list
        a list of all employes
    returns : list, 
        a list of all employes with CRUD oprtions and detail view
    """

    employeef_list = Employee.objects.all()
    employeef_filter = EmployeeFilter(request.GET, queryset= employeef_list)
    return render(request, 'TaskManagement/employee_list.html', {'filter': employeef_filter})

"""
    A class used to view employee detail.
    ...

    Attributes
    ----------
    model : 
        Employee
    template_name :
        'TaskManagement/employee_detail.html'

    created by :
    -------
        Sittana Afifi

    creation date : 
    -------
        06-Dec-2021

    update date :
    -------
         21-Jan-2022
"""
# view details of the specific employee.
class EmployeeDetailView(LoginRequiredMixin,generic.DetailView):
    logger.info("Enter EmployeeDetailView.")
    model = Employee
    template_name ='TaskManagement/employee_detail.html'

"""
    A class used to delete employee.
    ...

    Attributes
    ----------
    model : 
        Employee

    created by :
    -------
        Sittana Afifi

    creation date : 
    -------
        06-Dec-2021

    update date :
    -------
         21-Jan-2022
"""

class EmployeeDelete(LoginRequiredMixin,DeleteView):
    logger.info("Enter EmployeeDelete.")
    model = Employee
    success_url = reverse_lazy('employee-filter')

""" 
    add new employee.
    ...

    Attributes
    ----------
    model : 
        Employee

    Methods
    ------- 
    get_form(self)
        "eman should update it"
    
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
class EmployeeCreateView(LoginRequiredMixin,CreateView):
    logger.info("Enter EmployeeCreateView.")
    model = Employee
    fields = ['user','Employee_id', 'Phone_number', 'date_joined']
    success_url = reverse_lazy('employee-filter')

    """ add detepicker input from bootstrap"""
    def get_form(self):
        """ "eman should update it".
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
        self : 
            self.instance is your current employee

        return:
        ----------
            Return form that contained "eman should update it".
        """
        logger.info("Enter get_form in EmployeeCreateView.")
        form = super().get_form()
        form.fields['date_joined'].widget = DatePickerInput(options={"format": "mm/dd/yyyy","autoclose": True})
        return form

""" 
    update employee's information.
    ...

    Attributes
    ----------
    model : 
        Employee

    Methods
    -------
    get_success_url(self)
        Determine the URL to redirect to when the form is successfully validated. 
    get_form(self)
        "eman should update it"
    
    created by :
    -------
        Sittana Afifi

    creation date : 
    -------
        06-Dec-2021

    update date :
    -------
         21-Jan-2022
"""
class EmployeeUpdateView(LoginRequiredMixin,UpdateView):
    logger.info("Enter EmployeeUpdateView.")
    model = Employee
    fields = ['Employee_id', 'Phone_number', 'date_joined']
    
    def get_success_url(self):
        """ Determine the URL to redirect to when the form is successfully validated.
        created by :
        -------
            Sittana Afifi

        creation date : 
        -------
            18-Dec-2021

        update date :
        -------
            21-Jan-2022

        Parameters
        ----------
        self : 
            self.instance is your current employee

        return:
        ----------
            Return resolving Django URL names into URL paths 'employee-detail'.
        """
        logger.info("Enter get_success_url.")
        return reverse('employee-detail',args= [str(self.object.id)])
    
    """ add detepicker input from bootstrap"""
    def get_form(self):
        """ "eman should update it".
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
        self : 
            self.instance is your current employee

        return:
        ----------
            Return form that contained "eman should update it".
        """
        form = super().get_form()
        form.fields['date_joined'].widget = DatePickerInput(options={"format": "mm/dd/yyyy","autoclose": True})
        return form

class ProjectListView(LoginRequiredMixin,generic.ListView):
    logger.info("Enter ProjectListView.")
    model = Project
    template_name = 'TaskManagement/project_list.html'
    paginate_by = 5
    filter_class = ProjectFilter

@login_required    
def ProjectViewFilter(request):
    """Project View filter for employee list and show filter options.

    Parameters
    ----------
    name : list
        a list of all projects
    returns : list, 
        a list of all projects with CRUD oprtions and detail view
    """

    project_list = Project.objects.all()
    project_filter = ProjectFilter(request.GET, queryset= project_list)
    return render(request, 'TaskManagement/project_list.html', {'filter': project_filter})

class ProjectDetailView(LoginRequiredMixin,generic.DetailView):
    logger.info("Enter ProjectDetailView.")
    model = Project
    template_name = 'TaskManagement/project_detail.html'

class ProjectCreate(LoginRequiredMixin,CreateView):
    logger.info("Enter ProjectCreate.")
    model = Project
    fields = '__all__'

class ProjectUpdate(LoginRequiredMixin,UpdateView):
    logger.info("Enter ProjectUpdate.")
    model = Project
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class ProjectDelete(LoginRequiredMixin,DeleteView):
    logger.info("Enter ProjectDelete.")
    model = Project
    success_url = reverse_lazy('project-filter')

class TaskListView(LoginRequiredMixin,generic.ListView):
    logger.info("Enter TaskListView.")
    model = Task
    template_name = 'TaskManagement/task_list.html'
    paginate_by = 5
    filter_class = TaskFilter

@login_required
def TaskViewFilter(request):
    """Task View filter for employee list and show filter options.

    Parameters
    ----------
    name : list
        a list of all tasks
    returns : list, 
        a list of all tasks with CRUD oprtions and detail view
    """

    task_list = Task.objects.all()
    task_filter = TaskFilter(request.GET, queryset= task_list)
    return render(request, 'TaskManagement/task_list.html', {'filter': task_filter})

class TaskDetailView(LoginRequiredMixin,generic.DetailView):
    logger.info("Enter TaskDetailView.")
    model = Task
    template_name = 'TaskManagement/task_detail.html'

class TaskCreate(LoginRequiredMixin,CreateView):
    logger.info("Enter TaskCreate.")
    model = Task
    fields = '__all__'

class TaskUpdate(LoginRequiredMixin,UpdateView):
    logger.info("Enter TaskUpdate.")
    model = Task
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class TaskDelete(LoginRequiredMixin,DeleteView):
    logger.info("Enter TaskDelete.")
    model = Task
    success_url = reverse_lazy('task-filter')

# Taskmanagment List View:
class TaskmanagmentListView(LoginRequiredMixin,generic.ListView):
    logger.info("Enter TaskmanagmentListView.")
    model = Taskmanagment
    template_name ='TaskManagement/taskmanagment_list.html'
    paginate_by = 5
    filter_class = TaskmanagmentFilter

@login_required  
def TaskmanagmentViewFilter(request):
    """Taskmanagment View filter for taskmanagment list and show filter options.

    Parameters
    ----------
    name : list
        a list of all assigned tasks
    returns : list, 
        a list of all assigned tasks with CRUD oprtions and detail view
    """
    
    taskmanagment_list = Taskmanagment.objects.all()
    taskmanagment_filter = TaskmanagmentFilter(request.GET, queryset= taskmanagment_list)
    return render(request, 'TaskManagement/taskmanagment_list.html', {'filter': taskmanagment_filter})
    
# Taskmanagment Details View:
class TaskmanagmentDetailView(LoginRequiredMixin,generic.DetailView):
    logger.info("Enter TaskmanagmentDetailView.")
    model = Taskmanagment
    template_name ='TaskManagement/taskmanagment_detail.html'

# Create a specific taskmanagment:
class TaskmanagmentCreate(LoginRequiredMixin,CreateView):
    logger.info("Enter TaskmanagmentCreate.")
    model = Taskmanagment
    fields = '__all__'

    """ add datepicker to the form """
    def get_form(self):
        form = super().get_form()
        form.fields['start_date'].widget = DatePickerInput(options={"format": "mm/dd/yyyy","autoclose": True})
        form.fields['end_date'].widget = DatePickerInput(options={"format": "mm/dd/yyyy","autoclose": True})
        return form
        
# Update a specific taskmanagment:
class TaskmanagmentUpdate(LoginRequiredMixin,UpdateView):
    logger.info("Enter TaskmanagmentUpdate.")
    model = Taskmanagment
    fields = ['assignee' , 'assigneedTo' , 'task_managment' , 'status' , 'priority' , 'comment' , 'start_date' , 'end_date' ]

    def form_valid(self, form):
        """Function to send emails after update Taskmanagment model.

    Parameters
    ----------
    subject : 
        str

    assignee : 
        forighn key from employee model
    
    assigneedTo : 
        manytomany field from employee model
    
    task_managment :
        charfield

    status  , priority and  comment :
        charfield
    
    start_date and  end_date:
        datefield
        
    returns : email, 
        send email address for the selected team email address.

    """

        subject = 'Update Assign Task Details'
        Assignee_Name = form.cleaned_data.get('assignee')
        AssignedTo_Team = form.cleaned_data.get('assigneedTo')
        [print(member.user.email) for member in AssignedTo_Team.all()]
        Task_Detail = form.cleaned_data.get('task_managment')
        Task_Start_Date = form.cleaned_data.get('start_date')
        Task_End_Date = form.cleaned_data.get('end_date') 
        Task_Priority = form.cleaned_data.get('priority')
        Task_Status = form.cleaned_data.get('status')
        Comments = form.cleaned_data.get('comment')
        email_from = settings.EMAIL_HOST_USER
        message = f'Dear All:\n  Have a good day this email due to update task details {Task_Detail} created by {Assignee_Name}, The task will start at {Task_Start_Date} and end at {Task_End_Date} with {Task_Priority} priority and status {Task_Status}. \n {Comments}.\n (H) means High,\n (L) means Low, \n (M) means meduim priorities.\n (TD) means To Do,\n (IP) means In Progress, \n (C) means Completed For status.\n\n \n Best Regards'
        recipient_list = [ (member.user.email) for member in AssignedTo_Team.all() ]
        send_mail( subject, message, email_from, recipient_list )
        return super(TaskmanagmentUpdate, self).form_valid(form)
    
    """ add datepicker to the form """
    def get_form(self):
        form = super().get_form()
        form.fields['start_date'].widget = DatePickerInput(options={"format": "mm/dd/yyyy","autoclose": True})
        form.fields['end_date'].widget = DatePickerInput(options={"format": "mm/dd/yyyy","autoclose": True})
        return form

# Delete a specific taskmanagment:
class TaskmanagmentDelete(LoginRequiredMixin,DeleteView):
    logger.info("Enter TaskmanagmentDelete.")
    model = Taskmanagment
    success_url = reverse_lazy('taskmanagment-filter')

"""
    A function used to Assign Task to the Team Form create view  for Metting Room.
    display the attributes of form and ask user to enter all requirements to assign task.
    ...

    Attributes
    ----------
    assignee : 
        forighn key from employee model
    
    assigneedTo : 
        manytomany field from employee model
    
    task_managment :
        charfield

    status  , priority and  comment :
        charfield
    
    start_date and  end_date:
        datefield

    Methods
    -------
        use assign task form

    output 
    -------
    details of the assigned tasks request and the staus if it success or failed.

    -------
    created by :
    -------
        Eman 

    creation date : 
    -------
        15-Dec-2021

    update date :
    -------
        20-Dec-2022
"""

@login_required
def assign_task_view(request):
    """Function to send emails after asign Taskmanagment model.

    Parameters
    ----------
    subject : 
        str

    assignee : 
        forighn key from employee model
    
    assigneedTo : 
        manytomany field from employee model
    
    task_managment :
        charfield

    status  , priority and  comment :
        charfield
    
    start_date and  end_date:
        datefield
        
    returns : email, 
        send email address for the selected team email address.

    """

    logger.info("Enter assign_task_view.")
    form = AssignTaskForm()
    if request.method == "POST":
        logger.info("The request is POST.")
        form = AssignTaskForm(request.POST)
        if form.is_valid():
            logger.info("Enter is valid.")
            form.save()
            subject = 'Assign Task Details'
            Assignee_Name = form.cleaned_data.get('assignee')
            AssignedTo_Team = form.cleaned_data.get('assigneedTo')
            [print(member.user.email) for member in AssignedTo_Team.all()]
            Task_Detail = form.cleaned_data.get('task_managment')
            Task_Start_Date = form.cleaned_data.get('start_date')
            Task_End_Date = form.cleaned_data.get('end_date') 
            Task_Priority = form.cleaned_data.get('priority')
            Task_Status = form.cleaned_data.get('status')
            Comments = form.cleaned_data.get('comment')
            email_from = settings.EMAIL_HOST_USER
            message = f'Dear All:\n  Have a good day this email due to new task details {Task_Detail} created by {Assignee_Name}, The task will start at {Task_Start_Date} and end at {Task_End_Date} with {Task_Priority} priority and status {Task_Status}. \n {Comments}.\n (H) means High,\n (L) means Low, \n (M) means meduim priorities.\n (TD) means To Do,\n (IP) means In Progress, \n (C) means Completed For status.\n\n \n Best Regards'
            recipient_list = [ (member.user.email) for member in AssignedTo_Team.all() ]
            send_mail( subject, message, email_from, recipient_list )
            return HttpResponseRedirect(reverse('taskmanagment-filter') )

    context = {
        'form' : form ,
        }

    return render(request, "TaskManagement/assign_task.html", context)

# -----------------------------------------------------------
# Assign Task to the Team Form update view  for Metting Room.
# display the attributes of form and ask user to enter all requirements to assign task.
# created by : Eman 
# creation date : -Dec-2021
# update date : -Dec-2022
# parameters : modelchoice , datefield input , multiple choices for team , charfiled 
# task creater , assignees of the task  , task name if it addhoc tasks or project name
# task status and the priority of it , start and end date of the task finally addtional comments.
# output: details of the assigned tasks request and the staus if it success or failed.
# -----------------------------------------------------------

@login_required
def update_assign_task_view(request, pk):
    logger.info("Enter assign_task_view.")
    assign = Taskmanagment.objects.get(pk=pk)
    form = UpdateAssignTaskForm(request.POST or None,instance=assign)
    if request.method == "POST":
        logger.info("The request is POST.")
        form = UpdateAssignTaskForm(request.POST)
        if form.is_valid():
            logger.info("Enter is valid.")
            form.save()
            return HttpResponseRedirect(reverse('taskmanagment-filter') )
    context = {
        'form' : form ,
        }
    return render(request, "TaskManagement/update_assign_task.html", context)

today = _datetime.date.today()

"""
    A function used to export model information from database.
    ...

    Attributes
    ----------
    list : list
        the list of the employee
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
def export_employees_xls(request):
    """ Export all employee list details view from database and allow filter option
        with different firmat(excel , json , yaml) .

        If there is no filter option choosed all employee in database will be export.

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
    employeef_filter = EmployeeFilter(request.GET, queryset=Employee.objects.all())
    dataset = EmployeeResource().export(employeef_filter.qs)

    if file_format == 'CSV':
        logger.info("Export csv file format.")
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] ='attachment;filename={date}-Employees.csv'.format(date=today.strftime('%Y-%m-%d'),)  
        writer = csv.writer(response)
        writer.writerow(['User', 'Employee_id','Phone_Number', 'Date_Joined',])
        for std in dataset:
            writer.writerow(std)
        return response 

    elif file_format == 'JSON':
        logger.info("Export json file format.")
        response = HttpResponse(dataset.json, content_type='application/json')
        response['Content-Disposition'] = 'attachment;filename={date}-Employees.json'.format(date=today.strftime('%Y-%m-%d'),)  
        return response
    
    elif file_format == 'YAML':
        logger.info("Export yaml file format.")
        response = HttpResponse(dataset.yaml,content_type='application/x-yaml')
        response['Content-Disposition'] ='attachment;filename={date}-Employees.yaml'.format(date=today.strftime('%Y-%m-%d'),)  
        return response

    elif file_format == 'Excel':
        logger.info("Export excel file format.")
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment;filename={date}-Employees.xls'.format(date=today.strftime('%Y-%m-%d'),)  
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Employees')

        row_num = 0 # Sheet header, first row

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['User', 'Employee_id','Phone_Number', 'Date_Joined',]

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

"""
    A function used to export model information from database.
    ...

    Attributes
    ----------
    list : list
        the list of the project
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
def export_projects_xls(request):
    """ Export all projects list details view from database and allow filter option
        with different firmat(excel , json , yaml) .

        If there is no filter option choosed all projects in database will be export.

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
    project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
    dataset = ProjectResource().export(project_filter.qs)
    
    if file_format == 'CSV':
        logger.info("Export csv file format.")
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] ='attachment;filename={date}-Projects.csv'.format(date=today.strftime('%Y-%m-%d'),)  
        writer = csv.writer(response)
        writer.writerow(['Name', 'Description',])
        for std in dataset:
            writer.writerow(std)
        return response 

    elif file_format == 'JSON':
        logger.info("Export json file format.")
        response = HttpResponse(dataset.json, content_type='application/json')
        response['Content-Disposition'] = 'attachment;filename={date}-Projects.json'.format(date=today.strftime('%Y-%m-%d'),) 
        return response

    elif file_format == 'YAML':
        logger.info("Export yaml file format.")
        response = HttpResponse(dataset.yaml,content_type='application/x-yaml')
        response['Content-Disposition'] = 'attachment; filename={date}-Projects.yaml'.format(date=today.strftime('%Y-%m-%d'),)
        return response

    elif file_format == 'Excel':
        logger.info("Export excel file format.")
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment;filename={date}-Projects.xls'.format(date=today.strftime('%Y-%m-%d'),)  

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Projects')

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True 

        columns = ['Name', 'Description',]

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

"""
    A function used to export model information from database.
    ...

    Attributes
    ----------
    list : list
        the list of the task
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
def export_tasks_xls(request):
    """ Export all tasks list details view from database and allow filter option
        with different firmat(excel , json , yaml) .

        If there is no filter option choosed all tasks in database will be export.

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
    task_filter = TaskFilter(request.GET, queryset=Task.objects.all())
    dataset = TaskResource().export(task_filter.qs)
    
    if file_format == 'CSV':
        logger.info("Export csv file format.")
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] ='attachment;filename={date}-Tasks.csv'.format(date=today.strftime('%Y-%m-%d'),)  
        writer = csv.writer(response)
        writer.writerow(['Project', 'Task_Name','Task_Description',])
        for std in dataset:
            writer.writerow(std)
        return response

    elif file_format == 'JSON':
        logger.info("Export json file format.")
        response = HttpResponse(dataset.json, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename={date}-Tasks.json'.format(date=today.strftime('%Y-%m-%d'),)
        return response

    elif file_format == 'YAML':
        logger.info("Export yaml file format.")
        response = HttpResponse(dataset.yaml,content_type='application/x-yaml')
        response['Content-Disposition'] = 'attachment; filename={date}-Tasks.yaml'.format(date=today.strftime('%Y-%m-%d'),)
        return response
    
    elif file_format == 'Excel':
        logger.info("Export excel file format.")
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment;filename={date}-Tasks.xls'.format(date=today.strftime('%Y-%m-%d'),)  

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Tasks')

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['Project', 'Task_Name','Task_Description',]

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

"""
    A function used to export model information from database.
    ...

    Attributes
    ----------
    list : list
        the list of the assig task
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
def export_taskmanagment_xls(request):
    """ Export all assign task list details view from database and allow filter option
        with different firmat(excel , json , yaml) .

        If there is no filter option choosed all assign tasks in database will be export.

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
    taskmanagment_filter = TaskmanagmentFilter(request.GET, queryset=Taskmanagment.objects.all())
    dataset = TaskmanagmentResource().export(taskmanagment_filter.qs)    
    
    if file_format == 'CSV':
        logger.info("Export csv file format.")
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] ='attachment;filename={date}-Tasks_Managment.csv'.format(date=today.strftime('%Y-%m-%d'),)  
        writer = csv.writer(response)
        writer.writerow(['Assignee', 'AssigneedTo','Task_Managment','Status','Priority','Start_Date', 'End_Date', 'Comment',])
        for std in dataset:
            writer.writerow(std)
        return response

    elif file_format == 'JSON':
        logger.info("Export json file format.")
        response = HttpResponse(dataset.json, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename={date}-Tasks_Managment.json'.format(date=today.strftime('%Y-%m-%d'),)
        return response

    elif file_format == 'YAML':
        logger.info("Export yaml file format.")
        response = HttpResponse(dataset.yaml,content_type='application/x-yaml')
        response['Content-Disposition'] = 'attachment; filename={date}-Tasks_Managment.yaml'.format(date=today.strftime('%Y-%m-%d'),)
        return response
    
    elif file_format == 'Excel':
        logger.info("Export excel file format.")
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment;filename={date}-Tasks_Managment.xls'.format(date=today.strftime('%Y-%m-%d'),)  

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Tasksmanagment')

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['Assignee', 'AssigneedTo','Task_Managment','Status','Priority','Start_Date', 'End_Date', 'Comment',]

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
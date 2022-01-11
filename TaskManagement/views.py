from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from .models import Employee , Taskmanagment
from django.views.generic.edit import UpdateView , DeleteView , CreateView 
from .models import Project, Task, Taskmanagment
from django.contrib.auth.decorators import login_required, permission_required
from django import forms
from .forms import AssignTaskForm
import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput
from flatpickr import DatePickerInput, TimePickerInput, DateTimePickerInput
from flatpickr.utils import GenericViewWidgetMixin
import os, logging, logging.config # Logging view in Django:
from django.http import HttpResponse

# Create a logger for this file or the name of the log level or Get an instance of a logger
logger = logging.getLogger(__name__) 
logger = logging.getLogger(__file__)

# view a list of all employees.
class EmployeesListView(LoginRequiredMixin,generic.ListView):
    logger.info("Enter EmployeesListView.")
    model = Employee
    template_name ='TaskManagement/employee_list.html'
    paginate_by = 5

# view details of the specific employee.
class EmployeeDetailView(generic.DetailView):
    logger.info("Enter EmployeeDetailView.")
    model = Employee
    template_name ='TaskManagement/employee_detail.html'

# delete specific employee.
class EmployeeDelete(DeleteView):
    logger.info("Enter EmployeeDelete.")
    model = Employee
    success_url = reverse_lazy('employee_list')

# Add specific employee.
class EmployeeCreateView(CreateView):
    logger.info("Enter EmployeeCreateView.")
    model = Employee
    fields = ['user','Employee_id', 'Phone_number', 'date_joined']
    success_url = reverse_lazy('employee_list')

    def get_form(self):
        form = super().get_form()
        form.fields['date_joined'].widget = DatePickerInput(options={"format": "mm/dd/yyyy","autoclose": True})
        return form

# update specific employee.
class EmployeeUpdateView(UpdateView):
    logger.info("Enter EmployeeUpdateView.")
    model = Employee
    fields = ['Employee_id', 'Phone_number', 'date_joined']
    
    def get_success_url(self):
        logger.info("Enter get_success_url.")
        return reverse('employee-detail',args= [str(self.object.id)])
    
    def get_form(self):
        form = super().get_form()
        form.fields['date_joined'].widget = DatePickerInput(options={"format": "mm/dd/yyyy","autoclose": True})
        return form


class ProjectListView(LoginRequiredMixin,generic.ListView):
    logger.info("Enter ProjectListView.")
    model = Project
    template_name = 'TaskManagement/project_list.html'
    paginate_by = 5

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
    success_url = reverse_lazy('projects')

class TaskListView(LoginRequiredMixin,generic.ListView):
    logger.info("Enter TaskListView.")
    model = Task
    template_name = 'TaskManagement/task_list.html'
    paginate_by = 5

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
    success_url = reverse_lazy('tasks')

# Taskmanagment List View:
class TaskmanagmentListView(LoginRequiredMixin,generic.ListView):
    logger.info("Enter TaskmanagmentListView.")
    model = Taskmanagment
    template_name ='TaskManagement/taskmanagment_list.html'
    paginate_by = 5
    
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
    
    def get_form(self):
        form = super().get_form()
        form.fields['start_date'].widget = DatePickerInput(options={"format": "mm/dd/yyyy","autoclose": True})
        form.fields['end_date'].widget = DatePickerInput(options={"format": "mm/dd/yyyy","autoclose": True})
        return form

# Delete a specific taskmanagment:
class TaskmanagmentDelete(LoginRequiredMixin,DeleteView):
    logger.info("Enter TaskmanagmentDelete.")
    model = Taskmanagment
    success_url = reverse_lazy('taskmanagments')

# Define Assign Task Form Create View : 
@login_required
def assign_task_view(request):
    logger.info("Enter assign_task_view.")
    form = AssignTaskForm()
    if request.method == "POST":
        logger.info("The request is POST.")
        form = AssignTaskForm(request.POST)
        if form.is_valid():
            logger.info("Enter is valid.")
            form.save()
            return HttpResponseRedirect(reverse('taskmanagments') )
    context = {
        'form' : form ,
        }
    return render(request, "TaskManagement/assign_task.html", context)

# Define Assign Task Form Update View : 
@login_required
def update_assign_task_view(request, pk):
    logger.info("Enter assign_task_view.")
    assign = Taskmanagment.objects.get(pk=pk)
    form = AssignTaskForm(request.POST or None,instance=assign)
    if request.method == "POST":
        logger.info("The request is POST.")
        form = AssignTaskForm(request.POST)
        if form.is_valid():
            logger.info("Enter is valid.")
            form.save()
            return HttpResponseRedirect(reverse('taskmanagments') )
    context = {
        'form' : form ,
        }
    return render(request, "TaskManagement/update_assign_task.html", context)
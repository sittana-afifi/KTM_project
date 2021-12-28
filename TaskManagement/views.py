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
from flatpickr import DatePickerInput, TimePickerInput, DateTimePickerInput
import os 
import logging
from django.http import HttpResponse
# or Get an instance of a logger:
logger = logging.getLogger(__name__)
import logging.config
logger = logging.getLogger(__file__)
from django.utils.log import DEFAULT_LOGGING


# view a list of all employees.
class EmployeesListView(LoginRequiredMixin,generic.ListView):
    model = Employee
    template_name ='TaskManagement/employee_list.html'



# view details of the specific employee.
class EmployeeDetailView(generic.DetailView):
    model = Employee
    template_name ='TaskManagement/employee_detail.html'



# delete specific employee.
class EmployeeDelete(DeleteView):
    model = Employee
    success_url = reverse_lazy('employee_list')


# Add specific employee.
class EmployeeCreateView(CreateView):
    model = Employee
    fields = ['user','Employee_id', 'Phone_number', 'date_joined']
    success_url = reverse_lazy('employee_list')



# update specific employee.
class EmployeeUpdateView(UpdateView):
    model = Employee
    fields = ['Employee_id', 'Phone_number', 'date_joined']
    def get_success_url(self):
        return reverse('employee-detail',args= [str(self.object.id)]) 

    

#####################################################
class ProjectListView(LoginRequiredMixin,generic.ListView):
    model = Project
    template_name = 'TaskManagement/project_list.html'

class ProjectDetailView(LoginRequiredMixin,generic.DetailView):
    model = Project
    template_name = 'TaskManagement/project_detail.html'

class ProjectCreate(LoginRequiredMixin,CreateView):
    model = Project
    fields = '__all__'

class ProjectUpdate(LoginRequiredMixin,UpdateView):
    model = Project
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class ProjectDelete(LoginRequiredMixin,DeleteView):
    model = Project
    success_url = reverse_lazy('projects')

#####################################################
class TaskListView(LoginRequiredMixin,generic.ListView):
    model = Task
    template_name = 'TaskManagement/task_list.html'

class TaskDetailView(LoginRequiredMixin,generic.DetailView):
    model = Task
    template_name = 'TaskManagement/task_detail.html'

class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    fields = '__all__'

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task
    success_url = reverse_lazy('tasks')

#######################################################

# Taskmanagment List View:
class TaskmanagmentListView(LoginRequiredMixin,generic.ListView):
    model = Taskmanagment
    template_name ='TaskManagement/taskmanagment_list.html'


# Taskmanagment Details View:
class TaskmanagmentDetailView(LoginRequiredMixin,generic.DetailView):
    model = Taskmanagment
    template_name ='TaskManagement/taskmanagment_detail.html'


# Create a specific taskmanagment:
class TaskmanagmentCreate(LoginRequiredMixin,CreateView):
    model = Taskmanagment
    fields = '__all__'


# Update a specific taskmanagment:
class TaskmanagmentUpdate(LoginRequiredMixin,UpdateView):
    model = Taskmanagment
    fields = '__all__' # Not recommended (potential security issue if more fields added)


# Delete a specific taskmanagment:
class TaskmanagmentDelete(LoginRequiredMixin,DeleteView):
    model = Taskmanagment
    success_url = reverse_lazy('taskmanagments')

#######################################################

# Define Assign Task Form View : 
@login_required
def assign_task_view(request):
    form = AssignTaskForm(request.POST)
    if request.method == "POST":
        form = AssignTaskForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('taskmanagments') )
    context = {
        'form' : form ,
        }
    return render(request, "TaskManagement/assign_task.html", context)


from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from .models import Employee , Taskmanagment
from django.views.generic.edit import UpdateView , DeleteView , CreateView 
from .models import Project, Task, Taskmanagment



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
    success_url = reverse_lazy('employee_list')
    

#####################################################
class ProjectListView(generic.ListView):
    model = Project
    template_name = 'TaskManagement/project_list.html'

class ProjectDetailView(generic.DetailView):
    model = Project
    template_name = 'TaskManagement/project_detail.html'

class ProjectCreate(CreateView):
    model = Project
    fields = '__all__'

class ProjectUpdate(UpdateView):
    model = Project
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('projects')

#######################################################
# Taskmanagment List View:
class TaskmanagmentListView(generic.ListView):
    model = Taskmanagment
    template_name ='TaskManagement/taskmanagment_list.html'


# Taskmanagment Details View:
class TaskmanagmentDetailView(generic.DetailView):
    model = Taskmanagment
    template_name ='TaskManagement/taskmanagment_detail.html'


# Create a specific taskmanagment:
class TaskmanagmentCreate(CreateView):
    model = Taskmanagment
    fields = '__all__'


# Update a specific taskmanagment:
class TaskmanagmentUpdate(UpdateView):
    model = Taskmanagment
    fields = '__all__' # Not recommended (potential security issue if more fields added)


# Delete a specific taskmanagment:
class TaskmanagmentDelete(DeleteView):
    model = Taskmanagment
    success_url = reverse_lazy('taskmanagments')


#####################################################
class TaskListView(generic.ListView):
    model = Task
    template_name = 'TaskManagement/task_list.html'

class TaskDetailView(generic.DetailView):
    model = Task
    template_name = 'TaskManagement/task_detail.html'

class TaskCreate(CreateView):
    model = Task
    fields = '__all__'

class TaskUpdate(UpdateView):
    model = Task
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class TaskDelete(DeleteView):
    model = Task
    success_url = reverse_lazy('tasks')

#######################################################

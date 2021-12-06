from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from .models import Employee 
from django.views.generic.edit import UpdateView , DeleteView , CreateView 
from django.views import generic




# view a list of all employees.
class EmployeesListView(PermissionRequiredMixin,generic.ListView):

    permission_required = 'catalog.can_mark_returned'
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
    
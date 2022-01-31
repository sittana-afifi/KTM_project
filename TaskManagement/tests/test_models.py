from django.test import TestCase
from TaskManagement.admin import EmployeeAdmin
#from TaskManagement.models import Employee
from TaskManagement.models import Employee,Project,Task
from TaskManagement.models import Employee, Taskmanagment
from django.contrib.auth.models import User

class TaskModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Task.objects.create(task_name='firstone', task_description='Taskfortest')
    
    def test_name_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('task_name').verbose_name
        self.assertEqual(field_label, 'task name')
    
    def test_description_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('task_description').verbose_name
        self.assertEqual(field_label, 'task description')
    
    def test_get_absolute_url(self):
        task = Task.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(task.get_absolute_url(), '/en/TaskManagement/task/1/')

class  ProjectModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Project.objects.create(name='firstone', description='Projectfortest')
    
    def test_name_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')
    
    def test_description_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')
    
    def test_get_absolute_url(self):
        project = Project.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(project.get_absolute_url(), '/en/TaskManagement/project/1/')


class EmployeeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user1=User.objects.create_user('sonu','sonu@xyz.com','sn@pswrd')        
        t=Employee.objects.create(user=user1, Employee_id='1111',Phone_number='0911111111')
        print(t.Employee_id)
    
    def test_Employee_id_label(self):
        Employee1 = Employee.objects.get(id=1)
        field_label = Employee1._meta.get_field('Employee_id').verbose_name
        self.assertEqual(field_label, 'Employee id')

    def test_Phone_number_label(self):
        Employee1 = Employee.objects.get(id=1)
        field_label = Employee1._meta.get_field('Phone_number').verbose_name
        self.assertEqual(field_label, 'Phone number')

    def test_date_joined_label(self):
        Employee1 = Employee.objects.get(id=1)
        field_label = Employee1._meta.get_field('date_joined').verbose_name
        self.assertEqual(field_label, 'date joined')
    
    def test__str__(self):
        Employee1 = Employee.objects.get(id=1)
        self.assertEqual(str(Employee1),str(Employee1.user))

    def test_Employee_id_max_length(self):
        Employee1 = Employee.objects.get(id=1)
        max_length = Employee1._meta.get_field('Employee_id').max_length
        self.assertEqual(max_length, 4)

    def test_Phone_number_max_length(self):
        Employee1 = Employee.objects.get(id=1)
        max_length = Employee1._meta.get_field('Phone_number').max_length
        self.assertEqual(max_length, 10)

    


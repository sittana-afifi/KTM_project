from django.test import TestCase
from TaskManagement.admin import EmployeeAdmin
#from TaskManagement.models import Employee
from TaskManagement.models import Employee,Project,Task
from TaskManagement.models import Employee, Taskmanagment
from django.contrib.auth.models import User

#from accounts.models import Account
class TaskModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Task.objects.create(name='firstone', description='Taskfortest')
    
    def test_name_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')
    
    def test_description_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')
    
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

    

class TaskmanagmentTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user1=User.objects.create_user('sonu','sonu@xyz.com','sn@pswrd')
        user2=User.objects.create_user('user','sonu@xyz.com','sn@pswrd')
        empl=Employee.objects.create(user=user1, Employee_id='1',Phone_number='0111111111')
        empl2=Employee.objects.create(user=user2, Employee_id='2',Phone_number='0000000000')
        task1=Task.objects.create(task_name=testtask, task_description='testtask')
        Taskmanagment.objects.create(assignee='user1', assigneedTo='user2', task_managment = 'task1',status='TD', priority ='L',
        start_date = 'datetime.date.today()',end_date= 'datetime.date.today()')

    def test_task_name_label(self):
        taskmanagment = Taskmanagment.objects.get(id=1)
        field_label = taskmanagment._meta.get_field('task_managment').verbose_name
        self.assertEqual(field_label, 'task managment')

    def test_date_of_death_label(self):
        taskmanagment = Taskmanagment.objects.get(id=1)
        field_label = taskmanagment._meta.get_field('start_date').verbose_name
        self.assertEqual(field_label, 'datetime.date.today()')

    def test_get_absolute_url(self):
        taskmanagment = Taskmanagment.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(taskmanagment.get_absolute_url(), '/TaskManagement/taskmanagment/1')
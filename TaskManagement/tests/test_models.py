from django.test import TestCase
from TaskManagement.admin import EmployeeAdmin
#from TaskManagement.models import Employee
from TaskManagement.models import Employee
from django.contrib.auth.models import User

#from accounts.models import Account


class EmployeeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user1=User.objects.create_user('sonu','sonu@xyz.com','sn@pswrd')        
        Employee.objects.create(user=user1, Employee_id='1111',Phone_number='0911111111')

    
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

    
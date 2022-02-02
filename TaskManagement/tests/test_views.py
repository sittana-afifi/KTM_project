from django.test import TestCase
from django.urls import reverse
from TaskManagement.models import Employee
from django.contrib.auth.models import User


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


        

# class EmployeeListViewTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # Create 13 employees for pagination tests
#         number_of_employees = 10

#         for user_id in range(number_of_employees):
#             User.objects.create(
#                 username=f'TestUser{user_id}',
#                 #last_name=f'Surname {user_id}',
#             )
#         for emp_id in range(number_of_employees):
#             x = Employee.objects.create(
#                 user=User.objects.get(username=f'TestUser{emp_id}'),
#                 Employee_id=f'123{emp_id}'
#             )
#     def test_view_url_exists_at_desired_location(self):
#         response = self.client.get('/en/TaskManagement/employee/employeesfilter')
#         self.assertEqual(response.status_code, 200)
    
#     # def test_view_url_accessible_by_name(self):
#     #     response = self.client.get(reverse('employee-filter'))
#     #     self.assertEqual(response.status_code, 200)
    
#     # def test_view_uses_correct_template(self):
#     #     response = self.client.get(reverse('employee-filter'))
#     #     self.assertEqual(response.status_code, 200)
#     #     self.assertTemplateUsed(response, 'TaskManagement/employee_list.html')

from django.test import TestCase
from django.urls import reverse
from TaskManagement.models import Employee
from django.contrib.auth.models import User


class EmployeeListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 employees for pagination tests
        number_of_employees = 10

        for user_id in range(number_of_employees):
            User.objects.create(
                username=f'TestUser{user_id}',
                #last_name=f'Surname {user_id}',
            )
        for emp_id in range(number_of_employees):
            x = Employee.objects.create(
                user=User.objects.get(username=f'TestUser{emp_id}'),
                Employee_id=f'123{emp_id}'
            )
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/en/TaskManagement/employee/employeesfilter')
        self.assertEqual(response.status_code, 200)
    
    # def test_view_url_accessible_by_name(self):
    #     response = self.client.get(reverse('employee-filter'))
    #     self.assertEqual(response.status_code, 200)
    
    # def test_view_uses_correct_template(self):
    #     response = self.client.get(reverse('employee-filter'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'TaskManagement/employee_list.html')

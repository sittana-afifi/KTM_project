from gettext import install
from django.test import TestCase
from django.urls import reverse
from TaskManagement.models import Employee, Project
from django.contrib.auth.models import User
from novaclient import base, client


class EmployeeListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 employees for pagination tests
        number_of_employees = 10

        for emp_id in range(number_of_employees):
            x = Employee.objects.create(
                user=User.objects.get(username=f'TestUser{emp_id}'),
                Employee_id=f'123{emp_id}'
            )
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/en/TaskManagement/employee/employeesfilter')
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('employee-filter'))
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('employee-filter'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'TaskManagement/employee_list.html')

class ProjectListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 projects for pagination tests
        number_of_projects = 10
        for project_id in range(number_of_projects):
            x = Project.objects.create(
                user=User.objects.get(username=f'TestUser{project_id}'),
                Project_id=f'123{project_id}'
            )
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/en/projects/projectsfilter/')
        self.assertEqual(response.status_code, 200)    
    
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('project-filter'))
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('project-filter'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'TaskManagement/project_list.html')  


class TaskListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 Tasks for pagination tests
        number_of_projects = 10
       
        for task_id in range(number_of_projects):
            x = Project.objects.create(
                user=User.objects.get(username=f'TestUser{task_id}'),
                Task_id=f'123{task_id}'
            )
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/en/tasks/tasksfilter/')
        self.assertEqual(response.status_code, 200)    
    
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('task-filter'))
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('task-filter'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'TaskManagement/task_list.html')                

                     

 
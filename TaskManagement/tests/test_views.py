from gettext import install
from django.test import TestCase
from django.urls import reverse
from TaskManagement.models import Employee, Project
from TaskManagement.models import Taskmanagment,Task
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
        for user_id in range(number_of_projects):
            User.objects.create(
                username=f'TestUser{user_id}',
                #last_name=f'Surname {user_id}',
            )
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
        for user_id in range(number_of_projects):
            User.objects.create(
                username=f'TestUser{user_id}',
                #last_name=f'Surname {user_id}',
            )
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

                     

 
'''
class TaskmanagmentListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 10 TaskmanagmentListView for pagination tests
        number_of_taskmanagment = 10

        for taskmanagment_id in range(number_of_taskmanagments):
            Taskmanagment.objects.create(assignee='user1', assigneedTo='user2', task_managment = 'task1',status='TD', priority ='L',
             start_date = 'datetime.date.today()',end_date= 'datetime.date.today()')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('taskmanagments/taskmanagmentsfilter/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('taskmanagment-filter'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('taskmanagment-filter'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'TaskManagement/taskmanagment_list.html')

    def test_pagination_is_2(self):
        response = self.client.get(reverse('taskmanagment-filter'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['taskmanagment_list']), 5)

    def test_lists_all_taskmanagment_filter(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('taskmanagment-filter')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['taskmanagment_list']), 5)
'''
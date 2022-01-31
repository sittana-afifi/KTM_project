from django.urls import  path
from TaskManagement import views

urlpatterns = [

    path('employee', views.EmployeesListView.as_view(), name='employee_list'),
    path('employee/employeesfilter', views.EmployeeViewFilter, name='employee-filter'),
    path('employees/export/xls/', views.export_employees_xls, name='export_employees_xls'),
    path('employee/detail/<int:pk>/', views.EmployeeDetailView.as_view(), name='employee-detail'),
    path('employee/<int:pk>/update/', views.EmployeeUpdateView.as_view(), name='employee-update'),
    path('employee/<int:pk>/delete/', views.EmployeeDelete.as_view(), name='employee-delete'),
    path('employee/create/', views.EmployeeCreateView.as_view(), name='employee-create'),
    path('projects/', views.ProjectListView.as_view(), name='projects'),
    path('projects/projectsfilter/', views.ProjectViewFilter, name='project-filter'),
    path('projects/export/xls/', views.export_projects_xls, name='export_projects_xls'),
    path('project/<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('project/create/', views.ProjectCreate.as_view(), name='project-create'),
    path('project/<int:pk>/update/', views.ProjectUpdate.as_view(), name='project-update'),
    path('project/<int:pk>/delete/', views.ProjectDelete.as_view(), name='project-delete'),
    path('tasks/', views.TaskListView.as_view(), name='tasks'),
    path('tasks/tasksfilter/', views.TaskViewFilter, name='task-filter'),
    path('task/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('task/create/', views.TaskCreate.as_view(), name='task-create'),
    path('task/<int:pk>/update/', views.TaskUpdate.as_view(), name='task-update'),
    path('task/<int:pk>/delete/', views.TaskDelete.as_view(), name='task-delete'),
    path('taskmanagments/', views.TaskmanagmentListView.as_view(), name='taskmanagments'),
    path('taskmanagments/taskmanagmentsfilter/', views.TaskmanagmentViewFilter, name='taskmanagment-filter'),
    path('taskmanagment/<int:pk>/', views.TaskmanagmentDetailView.as_view(), name='taskmanagment-detail'),
    path('taskmanagment/create/', views.TaskmanagmentCreate.as_view(), name='taskmanagment-create'),
    path('taskmanagment/<int:pk>/update/', views.TaskmanagmentUpdate.as_view(), name='taskmanagment-update'),
    path('taskmanagment/<int:pk>/delete/', views.TaskmanagmentDelete.as_view(), name='taskmanagment-delete'),
    path('taskmanagment/assign/', views.assign_task_view,  name='assign-task'),
    path('taskmanagment/assign/<int:pk>/update/', views.update_assign_task_view,  name='assign-task-update'),
    path('tasks/export/xls/', views.export_tasks_xls, name='export_tasks_xls'),
    path('taskmanagments/export/xls/', views.export_taskmanagment_xls, name='export_taskmanagment_xls'),

]
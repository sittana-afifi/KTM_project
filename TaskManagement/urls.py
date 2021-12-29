from django.urls import include, path
from TaskManagement import views


urlpatterns = [
    path('employee', views.EmployeesListView.as_view(), name='employee_list'),
    path('employee/detail/<int:pk>/', views.EmployeeDetailView.as_view(), name='employee-detail'),
    path('employee/<int:pk>/update/', views.EmployeeUpdateView.as_view(), name='employee-update'),
    path('employee/<int:pk>/delete/', views.EmployeeDelete.as_view(), name='employee-delete'),
    path('employee/create/', views.EmployeeCreateView.as_view(), name='employee-create'),
    path('projects/', views.ProjectListView.as_view(), name='projects'),
    path('project/<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('project/create/', views.ProjectCreate.as_view(), name='project-create'),
    path('project/<int:pk>/update/', views.ProjectUpdate.as_view(), name='project-update'),
    path('project/<int:pk>/delete/', views.ProjectDelete.as_view(), name='project-delete'),
    path('tasks/', views.TaskListView.as_view(), name='tasks'),
    path('task/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('task/create/', views.TaskCreate.as_view(), name='task-create'),
    path('task/<int:pk>/update/', views.TaskUpdate.as_view(), name='task-update'),
    path('task/<int:pk>/delete/', views.TaskDelete.as_view(), name='task-delete'),
    path('taskmanagments/', views.TaskmanagmentListView.as_view(), name='taskmanagments'),
    path('taskmanagment/<int:pk>/', views.TaskmanagmentDetailView.as_view(), name='taskmanagment-detail'),
    path('taskmanagment/create/', views.TaskmanagmentCreate.as_view(), name='taskmanagment-create'),
    path('taskmanagment/<int:pk>/update/', views.TaskmanagmentUpdate.as_view(), name='taskmanagment-update'),
    path('taskmanagment/<int:pk>/delete/', views.TaskmanagmentDelete.as_view(), name='taskmanagment-delete'),
    path('taskmanagment/assign/', views.assign_task_view,  name='assign-task'),
    path('taskmanagment/assign/<int:pk>/update/', views.update_assign_task_view,  name='assign-task-update'),

]

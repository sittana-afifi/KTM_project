from django.urls import include, path
from TaskManagement import views

urlpatterns = [
    path('', views.EmployeesListView.as_view(), name='employee_list'),
    path('detail/<int:pk>/', views.EmployeeDetailView.as_view(), name='employee-detail'),
    path('<int:pk>/update/', views.EmployeeUpdateView.as_view(), name='employee-update'),
    path('<int:pk>/delete/', views.EmployeeDelete.as_view(), name='employee-delete'),
    path('create/', views.EmployeeCreateView.as_view(), name='employee-create'),
    path('projects/', views.ProjectListView.as_view(), name='projects'),
    path('project/<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('project/create/', views.ProjectCreate.as_view(), name='project-create'),
    path('project/<int:pk>/update/', views.ProjectUpdate.as_view(), name='project-update'),
    path('project/<int:pk>/delete/', views.ProjectDelete.as_view(), name='project-delete'),
    path('taskmanagments/', views.TaskmanagmentListView.as_view(), name='taskmanagments'),
    path('taskmanagments/', views.TaskmanagmentListView.as_view(), name='taskmanagments'),
    path('taskmanagment/<int:pk>/', views.TaskmanagmentDetailView.as_view(), name='taskmanagment-detail'),
    path('taskmanagment/create/', views.TaskmanagmentCreate.as_view(), name='taskmanagment-create'),
    path('taskmanagment/<int:pk>/update/', views.TaskmanagmentUpdate.as_view(), name='taskmanagment-update'),
    path('taskmanagment/<int:pk>/delete/', views.TaskmanagmentDelete.as_view(), name='taskmanagment-delete'),
]

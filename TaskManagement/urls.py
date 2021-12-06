from django.urls import include, path
from TaskManagement import views

urlpatterns = [
    path('', views.EmployeesListView.as_view(), name='employee_list'),
    path('detail/<int:pk>/', views.EmployeeDetailView.as_view(), name='employee-detail'),
    path('<int:pk>/update/', views.EmployeeUpdateView.as_view(), name='employee-update'),
    path('<int:pk>/delete/', views.EmployeeDelete.as_view(), name='employee-delete'),
    path('create/', views.EmployeeCreateView.as_view(), name='employee-create'),
    path('taskmanagments/', views.TaskmanagmentListView.as_view(), name='taskmanagments'),
    path('taskmanagment/<int:pk>/', views.TaskmanagmentDetailView.as_view(), name='taskmanagment-detail'),
    path('taskmanagment/create/', views.TaskmanagmentCreate.as_view(), name='taskmanagment-create'),
    path('taskmanagment/<int:pk>/update/', views.TaskmanagmentUpdate.as_view(), name='taskmanagment-update'),
    path('taskmanagment/<int:pk>/delete/', views.TaskmanagmentDelete.as_view(), name='taskmanagment-delete'),


]

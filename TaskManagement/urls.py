from django.urls import include, path
from TaskManagement import views

urlpatterns = [
    path('', views.EmployeesListView.as_view(), name='employee_list'),
    path('detail/<int:pk>/', views.EmployeeDetailView.as_view(), name='employee-detail'),
    path('<int:pk>/update/', views.EmployeeUpdateView.as_view(), name='employee-update'),
    path('<int:pk>/delete/', views.EmployeeDelete.as_view(), name='employee-delete'),
    path('create/', views.EmployeeCreateView.as_view(), name='employee-create'),



]

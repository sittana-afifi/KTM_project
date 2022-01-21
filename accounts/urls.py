from django.urls import path
from accounts import views 

urlpatterns = [

    path('users', views.usersListView.as_view(), name='user_list'),
    path('users/usersfilter/', views.AccountViewFilter, name='user-filter'),
    path('usersfilter/export/xls/', views.export_users_xls, name='export_users_xls'),
    path('detail/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('<int:pk>/update/', views.UserUpdate.as_view(), name='user-update'),
    path('<int:pk>/delete/', views.UserDelete.as_view(), name='user-delete'),
    path('create/', views.createUser, name='get_user_info'),
    path('create1/', views.getUserInfoFromLDAP, name='user-create'),
    path('create2/', views.submitUserForm, name='usersubmitform'),

]

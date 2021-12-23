from django.conf.urls import handler404
from django.urls import include, path
from django.views.generic import RedirectView
from django.contrib import admin
from TaskManagement import forms
from accounts import views , forms

urlpatterns = [

    path('users', views.usersListView.as_view(), name='user_list'),
    path('detail/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('<int:pk>/update/', views.UserUpdate.as_view(), name='user-update'),
    path('<int:pk>/delete/', views.UserDelete.as_view(), name='user-delete'),
    path('create/', views.createUser, name='get_user_info'),
    path('create1/', views.getUserInfoFromLDAP, name='user-create'),
    path('create', views.submitUserForm, name='usersubmitform'),
    #path('create1/', views.moiz, name='moiz'),
    #path('search/', views.search, name='search'),

]

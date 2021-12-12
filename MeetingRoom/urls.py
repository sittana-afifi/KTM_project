from django.urls import include, path
from MeetingRoom import views


urlpatterns = [
   
    path('meetings/', views.MeetingListView.as_view(), name='meetings'),
    path('meeting/<int:pk>/', views.MeetingDetailView.as_view(), name='meeting-detail'),
    path('meeting/create/', views.MeetingCreate.as_view(), name='meeting-create'),
    path('meeting/<int:pk>/update/', views.MeetingUpdate.as_view(), name='meeting-update'),
    path('meeting/<int:pk>/delete/', views.MeetingDelete.as_view(), name='meeting-delete'),
   
]

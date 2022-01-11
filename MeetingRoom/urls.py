from django.urls import include, path
from MeetingRoom import views

urlpatterns = [
   
    path('meetings/', views.MeetingListView.as_view(), name='meetings'),
    path('meeting/<int:pk>/', views.MeetingDetailView.as_view(), name='meeting-detail'),
    path('meeting/create/', views.MeetingCreate.as_view(), name='meeting-create'),
    path('meeting/<int:pk>/update/', views.MeetingUpdate.as_view(), name='meeting-update'),
    path('meeting/<int:pk>/delete/', views.MeetingDelete.as_view(), name='meeting-delete'),
    path('reservationmeetingrooms/', views.ReservationMeetingRoomListView.as_view(), name='reservationmeetingrooms'),
    path('reservationmeetingroom/<int:pk>/', views.ReservationMeetingRoomDetailView.as_view(), name='reservationmeetingroom-detail'),
    path('reservationmeetingroom/<int:pk>/delete/', views.ReservationMeetingRoomDelete.as_view(), name='reservationmeetingroom-delete'),
    path('reservationmeetingroom/reserve/', views.reserve_view, name='reserve'),
    path('reservationmeetingroom/reserve/<int:pk>/update/', views.update_reserve_view, name='reserve-update'),
    path('reservationmeetingrooms/search/', views.search, name='search'),
   
]

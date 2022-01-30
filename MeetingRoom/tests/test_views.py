from gettext import install
from django.test import TestCase
from django.urls import reverse
from MeetingRoom.models import Meeting
from django.contrib.auth.models import User
from TaskManagement.models import  Employee, Task, Project, Taskmanagment
from django.shortcuts import render
from django.forms.utils import ErrorList
from MeetingRoom.forms import ReservationForm, UpdateReservationForm
from django.test import TestCase
import datetime
from django import forms
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.test import TestCase
from MeetingRoom.models import ReservationMeetingRoom, Meeting

class MeetingListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 meetings for pagination tests
        number_of_meetings = 10
        for user_id in range(number_of_meetings):
            User.objects.create(
                username=f'TestUser{user_id}',
                #last_name=f'Surname {user_id}',
            )
        for meeting_id in range(number_of_meetings):
            x = Meeting.objects.create(
                user=User.objects.get(username=f'TestUser{meeting_id}'),
                Meeting_id=f'123{meeting_id}'
            )
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/en/meetings/meetingsfilter/')
        self.assertEqual(response.status_code, 200)    
    
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('meetings-filter'))
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('meetings-filter'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'MeetingRoom/meeting_list.html')

'''
class ReservationMeetingRoomListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 reservationmeetingrooms for pagination tests
        number_of_reservationmeetingrooms = 2

            ReservationMeetingRoom.objects.create(
                meeting_room=f'HR {reservationmeetingroom_id}',
                reservation_date=f'2021-12-1 {reservationmeetingroom_id}',
                reservation_from_time = f'12:00 {reservationmeetingroom_id}',
                reservation_to_time =f'13:00 {reservationmeetingroom_id}',
                team = f'user1 {reservationmeetingroom_id}',
                meeting_project_name = f'ktm{reservationmeetingroom_id}',
                task_name = f'task1 {reservationmeetingroom_id}',
            )
            ReservationMeetingRoom.objects.create(
                meeting_room=f'BD {reservationmeetingroom_id}',
                reservation_date=f'2021-12-1 {reservationmeetingroom_id}',
                reservation_from_time = f'12:00 {reservationmeetingroom_id}',
                reservation_to_time =f'13:00 {reservationmeetingroom_id}',
                team = f'user1 {reservationmeetingroom_id}',
                meeting_project_name = f'ktm{reservationmeetingroom_id}',
                task_name = f'task1 {reservationmeetingroom_id}',
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('reservationmeetingrooms/reservefilter/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('reserve-filter'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('reserve-filter'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'MeetingRoom/reservationmeetingroom_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('reserve-filter'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['MeetingRoom/reservationmeetingroom_list.html']), 10)

    def test_lists_all_reservationmeetingrooms(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('reserve-filter')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['MeetingRoom/reservationmeetingroom_list.html']), 1)

'''
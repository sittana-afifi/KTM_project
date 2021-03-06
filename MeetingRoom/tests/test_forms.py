from django.test import TestCase
import datetime
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from MeetingRoom.forms import ReservationForm
from django.urls import  reverse


class ReservationFormTest(TestCase):

    def test_form_field_label(self):
        form = ReservationForm()
        self.assertTrue(form.fields['meeting_room'].label is None or form.fields['meeting_room'].label == 'meeting room')
    
    def test_form_date_in_past(self):
        date = datetime.date.today()  - datetime.timedelta(days=1)
        form = ReservationForm(data={'reservation_date': date})
        self.assertFalse(form.is_valid())  # the form is correct data date not accept in past date

    def setUp(self):
        # Create two users
        test_user1 = User.objects.create_user(username='eman', password='admin123')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()
    
    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='eman', password='admin123')
        response = self.client.get(reverse('reservationmeetingrooms'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'eman')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'MeetingRoom/reservationmeetingroom_list.html')
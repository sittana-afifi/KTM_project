from gettext import install
from django.test import TestCase
from django.urls import reverse
from MeetingRoom.models import Meeting
from django.contrib.auth.models import User




class MeetingListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 meetings for pagination tests
        number_of_meetings = 10
           
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


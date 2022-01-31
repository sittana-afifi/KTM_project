from django.test import TestCase
from MeetingRoom.models import  Meeting

class MeetingModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Meeting.objects.create(name='firstone', description='Meetingroomfortest')
    
    def test_name_label(self):
        meeting = Meeting.objects.get(id=1)
        field_label = meeting._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')
    
    def test_description_label(self):
        meeting = Meeting.objects.get(id=1)
        field_label = meeting._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')
    
    def test_get_absolute_url(self):
        meeting = Meeting.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(meeting.get_absolute_url(), '/en/MeetingRoom/meeting/1/')

   

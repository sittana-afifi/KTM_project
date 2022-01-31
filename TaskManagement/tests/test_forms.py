import datetime
from django.test import TestCase
from TaskManagement.forms import AssignTaskForm

class AssignTaskFormTest(TestCase):
    def test_start_date_field_label(self):
        form = AssignTaskForm()
        self.assertTrue(form.fields['start_date'].label is None or form.fields['start_date'].label == 'start_date')

    def test_start_date_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = AssignTaskForm(data={'start_date': date})
        self.assertFalse(form.is_valid())
    
    def test_start_date_in_future(self):
        date = datetime.date.today()  + datetime.timedelta(days=1)
        form = AssignTaskForm(data={'start_date': date})
        self.assertFalse(form.is_valid())


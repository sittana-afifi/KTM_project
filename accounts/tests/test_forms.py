# import datetime
# from django.http import HttpRequest

# from django.test import TestCase
# from django.utils import timezone
# from django.contrib.auth.models import User
# from accounts.forms import UserForm

# class UserFormTest(TestCase):
#         def setUp(self):
#         # Create a user
#             form = UserForm()
#             #self.user = User.objects.create_user(username='test', password='admin123')
#         def test_username_field(self):
#             user = User.objects.create_user(username='test', password='admin123')
#             request = HttpRequest()
#             request.POST = {
#             "user": user.username,
            
#         }
#             form = UserForm(request.POST, user=user)
#             self.assertEqual(form.fields['username'].label, 'test')
    

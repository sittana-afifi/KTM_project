from django.contrib.auth.models import User
from django.test import TestCase
from accounts.models import Account


# class AccountModelTest(TestCase):
#     # def test_create_user(self):
#     #     # params = depends on your basemanager’s create_user methods.
#     #     user = User.objects.create(**params)
#     #     self.assertEqual(user.pk, user.id)

#     # def test_get_absolute_url(self):
#     #         account = Account.objects.get(id=1)
#     #         # This will also fail if the urlconf is not defined.
#     #         self.assertEqual(account.get_absolute_url(), '/en/accounts/detail/1/')
#     @classmethod
#     def setUpTestData(cls):
#        cls.user = Account.objects.create(username="userJohnDoe", password="secretpassword", first_name="John", last_name="Doe")

#     def test_string_representation_of_Account(self):
#         expected_representation_Account = "userJohnDoe: John Doe"
#         self.assertEqual(expected_representation_Account, str(self.user))
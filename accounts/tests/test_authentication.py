from django.test import TestCase

from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models import Token, User


class AuthenticateTest(TestCase):
    def test_returns_None_if_no_such_token(self):
        result = PasswordlessAuthenticationBackend.authenticate(
            'no-such-token')
        self.assertIsNone(result)

    def test_returns_new_user_with_correct_email_if_token_exists(self):
        email = 'alice@example.com'
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(token.uid)
        new_user = User.objects.get(email=email)
        self.assertEqual(user, new_user)

    def test_returns_existing_user_with_correct_email_if_token_exists(self):
        email = 'alice@example.com'
        existing_user = User.objects.create(email=email)
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(token.uid)
        self.assertEqual(user, existing_user)


class GetUserTest(TestCase):
    def test_gets_user_by_email(self):
        User.objects.create(email='ex@example.com')
        desired_user = User.objects.create(email='alice@example.com')
        found_user = PasswordlessAuthenticationBackend.get_user(
            email='alice@example.com')
        self.assertEqual(desired_user, found_user)

    def test_returns_None_if_no_user_with_given_email(self):
        self.assertIsNone(
            PasswordlessAuthenticationBackend.get_user(email='NOPE'))

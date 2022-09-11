from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.authentication import serializers

User = get_user_model()

class UserChangePasswordSerializerTests(TestCase):

    def setUp(self):
        self.user_attributes = {
            'first_name': 'Mack',
            'last_name': 'AS',
            'email': 'mack@gmail.com',
            'password': 'Test@123',
        }
        self.serializer_data = {
            'password': 'Test2@123',
            'confirm_password': 'Test2@123',
        }
        self.user  = User.objects.create(**self.user_attributes)

    def test_user_change_password_valid(self):
        change_password_valid = self.serializer_data
        serializer = serializers.UserChangePasswordSerializer(data=change_password_valid, context={'user': self.user})
        self.assertTrue(serializer.is_valid())

    def test_user_change_password_invalid(self):
        change_password_invalid = self.serializer_data
        change_password_invalid['password'] = '123'
        change_password_invalid['confirm_password'] = '123'
        serializer = serializers.UserChangePasswordSerializer(data=change_password_invalid, context={'user': self.user})
        self.assertFalse(serializer.is_valid())

    def test_invalid_confirm_password_different_of_password(self):
        change_password_invalid = self.serializer_data
        change_password_invalid['confirm_password'] = '123'
        serializer = serializers.UserChangePasswordSerializer(data=change_password_invalid, context={'user': self.user})
        self.assertFalse(serializer.is_valid())

    def test_invalid_confirm_password_blank(self):
        change_password_invalid = self.serializer_data
        change_password_invalid['confirm_password'] = ''
        serializer = serializers.UserChangePasswordSerializer(data=change_password_invalid, context={'user': self.user})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(str(serializer.errors['confirm_password'][0]), "This field may not be blank.")

    def test_password_is_required(self):
        change_password_invalid = self.serializer_data
        del change_password_invalid['password']
        serializer = serializers.UserChangePasswordSerializer(data=change_password_invalid, context={'user': self.user})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['password']))
        self.assertEqual(str(serializer.errors['password'][0]), "This field is required.")

    def test_confirm_password_is_required(self):
        change_password_invalid = self.serializer_data
        del change_password_invalid['confirm_password']
        serializer = serializers.UserChangePasswordSerializer(data=change_password_invalid, context={'user': self.user})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['confirm_password']))
        self.assertEqual(str(serializer.errors['confirm_password'][0]), "This field is required.")

    def test_password_and_confirm_password_is_required(self):
        serializer = serializers.UserChangePasswordSerializer(data={}, context={'user': self.user})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['password', 'confirm_password']))
        self.assertEqual(str(serializer.errors['password'][0]), "This field is required.")
        self.assertEqual(str(serializer.errors['confirm_password'][0]), "This field is required.")
from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.authentication import serializers
from apps.utils.response import error_messages

User = get_user_model()

class LoginSerializerTests(TestCase):

    def setUp(self):
        self.user_attributes = {
            'first_name': 'Mack',
            'last_name': 'AS',
            'email': 'mack@gmail.com',
            'password': '12345',
        }
        self.serializer_data = {
            'firstName': 'Zecha',
            'lastName': 'ZZ',
            'email': 'zecha@gmail.com',
            'password': '12345',
            'confirm_password': '12345',
        }
        self.user  = User.objects.create(**self.user_attributes)
        self.serializer = serializers.LoginSerializer(instance=self.user)

    def test_login_contains_expected_fields(self):
        data = self.serializer.data
        # self.assertEqual(set(data.keys()), set(['email', 'firstName', 'lastName']))
        self.assertCountEqual(data.keys(), ['email', 'password'])

    def test_login_fields_content(self):
        data = self.serializer.data
        self.assertEqual(data['email'], self.user_attributes['email'])
        self.assertEqual(data['password'], self.user_attributes['password'])

    def test_login_fields_is_required(self):
        serializer = serializers.LoginSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['email', 'password']))
        self.assertEqual(str(serializer.errors['email'][0]), error_messages('required', 'fr', 'email'))
        self.assertEqual(str(serializer.errors['password'][0]), error_messages('required', 'fr', 'Mot de passe'))

    def test_login_email_field_is_required(self):
        serializer_data = self.serializer_data
        del serializer_data['email']
        serializer = serializers.LoginSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['email']))
        self.assertEqual(str(serializer.errors['email'][0]), error_messages('required', 'fr', 'email'))

    def test_login_email_field_is_not_blank(self):
        serializer_data = self.serializer_data
        serializer_data['email'] = ''
        serializer = serializers.LoginSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['email']))
        self.assertEqual(str(serializer.errors['email'][0]), error_messages('blank', 'fr', 'email'))

    def test_login_email_field_is_valide(self):
        serializer_data = self.serializer_data
        serializer = serializers.LoginSerializer(data=serializer_data)
        self.assertTrue(serializer.is_valid())
        self.assertFalse(serializer.errors)
        self.assertEqual(serializer.errors, {})

    def test_login_password_field_is_required(self):
        serializer_data = self.serializer_data
        del serializer_data['password']
        serializer = serializers.LoginSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['password']))
        self.assertEqual(str(serializer.errors['password'][0]), error_messages('required', 'fr', 'Mot de passe'))

    def test_login_password_field_is_not_blank(self):
        serializer_data = self.serializer_data
        serializer_data['password'] = ''
        serializer = serializers.LoginSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['password']))
        self.assertEqual(str(serializer.errors['password'][0]), error_messages('blank', 'fr', 'Mot de passe'))

    def test_login_password_field_is_valide(self):
        serializer_data = self.serializer_data
        serializer = serializers.LoginSerializer(data=serializer_data)
        self.assertTrue(serializer.is_valid())
        self.assertFalse(serializer.errors)
        self.assertEqual(serializer.errors, {})
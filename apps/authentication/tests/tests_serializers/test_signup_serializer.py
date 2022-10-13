from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.authentication import serializers
from apps.utils.response import error_messages, response_messages

User = get_user_model()
res = response_messages('fr')

class SignupSerializerTests(TestCase):

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
            'password': 'Test@123',
            'confirmPassword': 'Test@123',
        }
        self.user  = User.objects.create(**self.user_attributes)
        self.serializer = serializers.SignupSerializer(instance=self.user)

    def test_signup_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['email', 'firstName', 'lastName'])

    def test_signup_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['firstName'], self.user_attributes['first_name'])
        self.assertEqual(data['lastName'], self.user_attributes['last_name'])
        self.assertEqual(data['email'], self.user_attributes['email'])

    def test_signup_fields_is_required(self):
        serializer = serializers.SignupSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['firstName', 'lastName', 'email', 'password', 'confirmPassword']))
        self.assertEqual(str(serializer.errors['firstName'][0]), error_messages('required', 'fr', 'Prénom'))
        self.assertEqual(str(serializer.errors['lastName'][0]), error_messages('required', 'fr', 'Nom'))
        self.assertEqual(str(serializer.errors['email'][0]), error_messages('required', 'fr', 'email'))
        self.assertEqual(str(serializer.errors['password'][0]), error_messages('required', 'fr', 'Mot de passe'))
        self.assertEqual(str(serializer.errors['confirmPassword'][0]), error_messages('required', 'fr', 'Confirmation mot de passe'))

    def test_signup_firstName_field_is_not_blank(self):
        serializer_data = self.serializer_data
        serializer_data['firstName'] = ''
        serializer_data['lastName'] = ''
        serializer_data['email'] = ''
        serializer_data['password'] = ''
        serializer_data['confirmPassword'] = ''
        serializer = serializers.SignupSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['firstName', 'lastName', 'email', 'password', 'confirmPassword']))
        self.assertEqual(str(serializer.errors['firstName'][0]), error_messages('blank', 'fr', 'Prénom'))
        self.assertEqual(str(serializer.errors['lastName'][0]), error_messages('blank', 'fr', 'Nom'))
        self.assertEqual(str(serializer.errors['email'][0]), error_messages('blank', 'fr', 'email'))
        self.assertEqual(str(serializer.errors['password'][0]), error_messages('blank', 'fr', 'Mot de passe'))
        self.assertEqual(str(serializer.errors['confirmPassword'][0]), error_messages('blank', 'fr', 'Confirmation mot de passe'))


    def test_signup_fields_is_valide(self):
        serializer_data = self.serializer_data
        serializer = serializers.SignupSerializer(data=serializer_data)
        self.assertTrue(serializer.is_valid())
        self.assertFalse(serializer.errors)
        self.assertEqual(serializer.errors, {})

    def test_signup_email_is_invalide(self):
        serializer_data = self.serializer_data
        serializer_data['email'] = 'test@gmail'
        serializer = serializers.SignupSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['email']))
        self.assertEqual(str(serializer.errors['email'][0]), res["ENTER_A_VALID_EMAIL_ADDRESS"])

    def test_signup_email_email_address_already_exists(self):
        serializer_data = self.serializer_data
        serializer_data['email'] = 'mack@gmail.com'
        serializer = serializers.SignupSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['email']))
        self.assertEqual(str(serializer.errors['email'][0]), res["USER_WITH_THIS_EMAIL_ADDRESS_ALREADY_EXISTS"])

    def test_signup_password_field_is_invalid(self):
        serializer_data = self.serializer_data
        serializer_data['password'] = '12345'
        serializer = serializers.SignupSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['password']))
        self.assertEqual(str(serializer.errors['password'][0]), res["INVALID_PASSWORD"])

    def test_signup_the_confirm_password_not_matches_the_password(self):
        serializer_data = self.serializer_data
        serializer_data['confirmPassword'] = '1234'
        serializer = serializers.SignupSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['non_field_errors']))
        self.assertEqual(str(serializer.errors['non_field_errors'][0]), res["PASSWORD_AND_PASSWORD_CONFIRM_NOT_MATCH"])

    def test_signup_that_the_data_is_registering_correctly(self):
        serializer_data = self.serializer_data
        serializer = serializers.SignupSerializer(data=serializer_data)
        self.assertTrue(serializer.is_valid())
        new_user = serializer.save()
        new_user.refresh_from_db()
        self.assertEqual(new_user.first_name, 'Zecha')
        self.assertEqual(new_user.last_name, 'ZZ')
        self.assertEqual(new_user.email, 'zecha@gmail.com')
from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.account import serializers

User = get_user_model()

class UserSignupSerializerTests(TestCase):

    def setUp(self):
        self.user_attributes = {
            'first_name': 'Mack',
            'last_name': 'AS',
            'email': 'mack@gmail.com',
            'password': '12345',
        }
        self.serializer_data = {
            'first_name': 'Zecha',
            'last_name': 'ZZ',
            'email': 'zecha@gmail.com',
            'password': '12345',
            'password2': '12345',
        }
        self.user  = User.objects.create(**self.user_attributes)
        self.serializer = serializers.UserSignupSerializer(instance=self.user)

    def test_signup_contains_expected_fields(self):
        data = self.serializer.data
        # self.assertEqual(set(data.keys()), set(['email', 'first_name', 'last_name']))
        self.assertCountEqual(data.keys(), ['email', 'first_name', 'last_name'])

    def test_signup_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['first_name'], self.user_attributes['first_name'])
        self.assertEqual(data['last_name'], self.user_attributes['last_name'])
        self.assertEqual(data['email'], self.user_attributes['email'])

    def test_signup_fields_is_required(self):
        serializer = serializers.UserSignupSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['first_name', 'last_name', 'email', 'password', 'password2']))
        self.assertEqual(str(serializer.errors['first_name'][0]), 'This field is required.')
        self.assertEqual(str(serializer.errors['last_name'][0]), 'This field is required.')
        self.assertEqual(str(serializer.errors['email'][0]), 'This field is required.')
        self.assertEqual(str(serializer.errors['password'][0]), 'This field is required.')
        self.assertEqual(str(serializer.errors['password2'][0]), 'This field is required.')

    def test_signup_first_name_field_is_required(self):
        serializer_data = self.serializer_data
        del serializer_data['first_name']
        serializer = serializers.UserSignupSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['first_name']))
        self.assertEqual(str(serializer.errors['first_name'][0]), 'This field is required.')

    def test_signup_first_name_field_is_not_blank(self):
        serializer_data = self.serializer_data
        serializer_data['first_name'] = ''
        serializer = serializers.UserSignupSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['first_name']))
        self.assertEqual(str(serializer.errors['first_name'][0]), 'This field may not be blank.')

    def test_signup_first_name_field_is_valide(self):
        serializer_data = self.serializer_data
        serializer = serializers.UserSignupSerializer(data=serializer_data)
        self.assertTrue(serializer.is_valid())
        self.assertFalse(serializer.errors)
        self.assertEqual(serializer.errors, {})

    def test_signup_last_name_field_is_required(self):
        serializer_data = self.serializer_data
        del serializer_data['last_name']
        serializer = serializers.UserSignupSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['last_name']))
        self.assertEqual(str(serializer.errors['last_name'][0]), 'This field is required.')

    def test_signup_last_name_field_is_not_blank(self):
        serializer_data = self.serializer_data
        serializer_data['last_name'] = ''
        serializer = serializers.UserSignupSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['last_name']))
        self.assertEqual(str(serializer.errors['last_name'][0]), 'This field may not be blank.')

    def test_signup_last_name_field_is_valide(self):
        serializer_data = self.serializer_data
        serializer = serializers.UserSignupSerializer(data=serializer_data)
        self.assertTrue(serializer.is_valid())
        self.assertFalse(serializer.errors)
        self.assertEqual(serializer.errors, {})

    def test_signup_email_field_is_required(self):
        serializer_data = self.serializer_data
        del serializer_data['email']
        serializer = serializers.UserSignupSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['email']))
        self.assertEqual(str(serializer.errors['email'][0]), 'This field is required.')

    def test_signup_email_field_is_not_blank(self):
        serializer_data = self.serializer_data
        serializer_data['email'] = ''
        serializer = serializers.UserSignupSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['email']))
        self.assertEqual(str(serializer.errors['email'][0]), 'This field may not be blank.')

    def test_signup_email_field_is_valide(self):
        serializer_data = self.serializer_data
        serializer = serializers.UserSignupSerializer(data=serializer_data)
        self.assertTrue(serializer.is_valid())
        self.assertFalse(serializer.errors)
        self.assertEqual(serializer.errors, {})

    def test_signup_password_field_is_required(self):
        serializer_data = self.serializer_data
        del serializer_data['password']
        serializer = serializers.UserSignupSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['password']))
        self.assertEqual(str(serializer.errors['password'][0]), 'This field is required.')

    def test_signup_password_field_is_not_blank(self):
        serializer_data = self.serializer_data
        serializer_data['password'] = ''
        serializer = serializers.UserSignupSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['password']))
        self.assertEqual(str(serializer.errors['password'][0]), 'This field may not be blank.')

    def test_signup_password_field_is_valide(self):
        serializer_data = self.serializer_data
        serializer = serializers.UserSignupSerializer(data=serializer_data)
        self.assertTrue(serializer.is_valid())
        self.assertFalse(serializer.errors)
        self.assertEqual(serializer.errors, {})

    def test_signup_password2_field_is_required(self):
        serializer_data = self.serializer_data
        del serializer_data['password2']
        serializer = serializers.UserSignupSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['password2']))
        self.assertEqual(str(serializer.errors['password2'][0]), 'This field is required.')

    def test_signup_password2_field_is_not_blank(self):
        serializer_data = self.serializer_data
        serializer_data['password2'] = ''
        serializer = serializers.UserSignupSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['password2']))
        self.assertEqual(str(serializer.errors['password2'][0]), 'This field may not be blank.')

    def test_signup_password2_field_is_valide(self):
        serializer_data = self.serializer_data
        serializer = serializers.UserSignupSerializer(data=serializer_data)
        self.assertTrue(serializer.is_valid())
        self.assertFalse(serializer.errors)
        self.assertEqual(serializer.errors, {})

    def test_signup_if_the_password2_matches_the_password(self):
        serializer_data = self.serializer_data
        serializer_data['password2'] = '1234'
        serializer = serializers.UserSignupSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['non_field_errors']))
        self.assertEqual(str(serializer.errors['non_field_errors'][0]), 'Le mot de passe et le mot de passe de confirmation ne correspondent pas.')

    def test_signup_if_the_password_matches_the_password2(self):
        serializer_data = self.serializer_data
        serializer_data['password'] = '1234'
        serializer = serializers.UserSignupSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['non_field_errors']))
        self.assertEqual(str(serializer.errors['non_field_errors'][0]), 'Le mot de passe et le mot de passe de confirmation ne correspondent pas.')

    def test_signup_that_the_data_is_registering_correctly(self):
        serializer_data = self.serializer_data
        serializer = serializers.UserSignupSerializer(data=serializer_data)
        self.assertTrue(serializer.is_valid())
        new_user = serializer.save()
        new_user.refresh_from_db()
        self.assertEqual(new_user.first_name, 'Zecha')
        self.assertEqual(new_user.last_name, 'ZZ')
        self.assertEqual(new_user.email, 'zecha@gmail.com')
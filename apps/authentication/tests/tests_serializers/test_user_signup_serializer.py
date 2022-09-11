from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.authentication import serializers

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
            'firstName': 'Zecha',
            'lastName': 'ZZ',
            'email': 'zecha@gmail.com',
            'password': 'Test@123',
            'confirmPassword': 'Test@123',
        }
        self.user  = User.objects.create(**self.user_attributes)
        self.serializer = serializers.UserSignupSerializer(instance=self.user)

    def test_signup_contains_expected_fields(self):
        data = self.serializer.data
        # self.assertEqual(set(data.keys()), set(['email', 'firstName', 'lastName']))
        self.assertCountEqual(data.keys(), ['email', 'firstName', 'lastName'])

    def test_signup_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['firstName'], self.user_attributes['first_name'])
        self.assertEqual(data['lastName'], self.user_attributes['last_name'])
        self.assertEqual(data['email'], self.user_attributes['email'])

    def test_signup_fields_is_required(self):
        serializer = serializers.UserSignupSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['firstName', 'lastName', 'email', 'password', 'confirmPassword']))
        self.assertEqual(str(serializer.errors['firstName'][0]), "This field is required.")
        self.assertEqual(str(serializer.errors['lastName'][0]), "This field is required.")
        self.assertEqual(str(serializer.errors['email'][0]), "This field is required.")
        self.assertEqual(str(serializer.errors['password'][0]), "This field is required.")
        self.assertEqual(str(serializer.errors['confirmPassword'][0]), "This field is required.")

    def test_signup_firstName_field_is_required(self):
        serializer_data = self.serializer_data
        del serializer_data['firstName']
        serializer = serializers.UserSignupSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['firstName']))
        self.assertEqual(str(serializer.errors['firstName'][0]), "This field is required.")

    def test_signup_firstName_field_is_not_blank(self):
        serializer_data = self.serializer_data
        serializer_data['firstName'] = ''
        serializer = serializers.UserSignupSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['firstName']))
        self.assertEqual(str(serializer.errors['firstName'][0]), "This field may not be blank.")

    def test_signup_firstName_field_is_valide(self):
        serializer_data = self.serializer_data
        serializer = serializers.UserSignupSerializer(data=serializer_data)
        self.assertTrue(serializer.is_valid())
        self.assertFalse(serializer.errors)
        self.assertEqual(serializer.errors, {})

    def test_signup_lastName_field_is_required(self):
        serializer_data = self.serializer_data
        del serializer_data['lastName']
        serializer = serializers.UserSignupSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['lastName']))
        self.assertEqual(str(serializer.errors['lastName'][0]), "This field is required.")

    def test_signup_lastName_field_is_not_blank(self):
        serializer_data = self.serializer_data
        serializer_data['lastName'] = ''
        serializer = serializers.UserSignupSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['lastName']))
        self.assertEqual(str(serializer.errors['lastName'][0]), "This field may not be blank.")

    def test_signup_lastName_field_is_valide(self):
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
        self.assertEqual(str(serializer.errors['email'][0]), "This field is required.")

    def test_signup_email_field_is_not_blank(self):
        serializer_data = self.serializer_data
        serializer_data['email'] = ''
        serializer = serializers.UserSignupSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['email']))
        self.assertEqual(str(serializer.errors['email'][0]), "This field may not be blank.")

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
        self.assertEqual(str(serializer.errors['password'][0]), "This field is required.")

    def test_signup_password_field_is_not_blank(self):
        serializer_data = self.serializer_data
        serializer_data['password'] = ''
        serializer = serializers.UserSignupSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['password']))
        self.assertEqual(str(serializer.errors['password'][0]), "This field may not be blank.")

    def test_signup_password_field_is_invalid(self):
        serializer_data = self.serializer_data
        serializer_data['password'] = '12345'
        serializer = serializers.UserSignupSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['password']))
        self.assertEqual(str(serializer.errors['password'][0]), "The password must contain at least 8 characters, at least one upper and lower case letter, one number and one special character.")

    def test_signup_password_field_is_valide(self):
        serializer_data = self.serializer_data
        serializer = serializers.UserSignupSerializer(data=serializer_data)
        self.assertTrue(serializer.is_valid())
        self.assertFalse(serializer.errors)
        self.assertEqual(serializer.errors, {})

    def test_signup_confirm_password_field_is_required(self):
        serializer_data = self.serializer_data
        del serializer_data['confirmPassword']
        serializer = serializers.UserSignupSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['confirmPassword']))
        self.assertEqual(str(serializer.errors['confirmPassword'][0]), "This field is required.")

    def test_signup_confirm_password_field_is_not_blank(self):
        serializer_data = self.serializer_data
        serializer_data['confirmPassword'] = ''
        serializer = serializers.UserSignupSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['confirmPassword']))
        self.assertEqual(str(serializer.errors['confirmPassword'][0]), "This field may not be blank.")

    def test_signup_confirm_password_field_is_valide(self):
        serializer_data = self.serializer_data
        serializer = serializers.UserSignupSerializer(data=serializer_data)
        self.assertTrue(serializer.is_valid())
        self.assertFalse(serializer.errors)
        self.assertEqual(serializer.errors, {})

    def test_signup_if_the_confirm_password_matches_the_password(self):
        serializer_data = self.serializer_data
        serializer_data['confirmPassword'] = '1234'
        serializer = serializers.UserSignupSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['non_field_errors']))
        self.assertEqual(str(serializer.errors['non_field_errors'][0]), "Password and Confirm Password doesn't match")

    def test_signup_if_the_password_matches_the_confirm_password(self):
        serializer_data = self.serializer_data
        serializer_data['password'] = 'Test@000'
        serializer = serializers.UserSignupSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        print("set(serializer.errors) : ", set(serializer.errors))
        self.assertEqual(set(serializer.errors), set(['non_field_errors']))
        self.assertEqual(str(serializer.errors['non_field_errors'][0]), "Password and Confirm Password doesn't match")

    def test_signup_that_the_data_is_registering_correctly(self):
        serializer_data = self.serializer_data
        serializer = serializers.UserSignupSerializer(data=serializer_data)
        self.assertTrue(serializer.is_valid())
        new_user = serializer.save()
        new_user.refresh_from_db()
        self.assertEqual(new_user.first_name, 'Zecha')
        self.assertEqual(new_user.last_name, 'ZZ')
        self.assertEqual(new_user.email, 'zecha@gmail.com')
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from apps.authentication import serializers
from apps.utils.response import res


User = get_user_model()


class UserResetPasswordSerializerTests(TestCase):

    def setUp(self):
        self.user_attributes = {
            'first_name': 'Mack',
            'last_name': 'AS',
            'email': 'mack@gmail.com',
            'password': '12345',
        }
        self.serializer_data = {
            'password': 'Test@123',
            'confirm_password': 'Test@123',
        }
        self.user  = User.objects.create(**self.user_attributes)
        self.uid = urlsafe_base64_encode(force_bytes(self.user.public_id))
        self.token = PasswordResetTokenGenerator().make_token(self.user)
    
    def test_user_reset_password_valid(self):
        new_password_valid = self.serializer_data
        serializer = serializers.UserResetPasswordSerializer(data=new_password_valid, context={'uid': self.uid, 'token': self.token})
        self.assertTrue(serializer.is_valid())
    
    def test_user_reset_password_invalid(self):
        new_password_valid = self.serializer_data
        new_password_valid['password'] = '123'
        new_password_valid['confirm_password'] = '123'
        serializer = serializers.UserResetPasswordSerializer(data=new_password_valid, context={'uid': self.uid, 'token': self.token})
        self.assertFalse(serializer.is_valid())
    
    def test_user_reset_password_fields_is_required(self):
        new_password_valid = self.serializer_data
        serializer = serializers.UserResetPasswordSerializer(data={}, context={'uid': self.uid, 'token': self.token})
        self.assertFalse(serializer.is_valid())
    
    def test_user_reset_confirm_password_invalid(self):
        new_password_valid = self.serializer_data
        new_password_valid['confirm_password'] = '123'
        serializer = serializers.UserResetPasswordSerializer(data=new_password_valid, context={'uid': self.uid, 'token': self.token})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(str(serializer.errors['non_field_errors'][0]), res["PASSWORD_AND_PASSWORD_CONFIRM_NOT_MATCH"])
    
    def test_user_reset_password_with_uid_invalid(self):
        new_password_valid = self.serializer_data
        self.uid = "ABC"
        serializer = serializers.UserResetPasswordSerializer(data=new_password_valid, context={'uid': self.uid, 'token': self.token})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(str(serializer.errors['non_field_errors'][0]), res["TOKEN_IS_NOT_VALID_OR_HAS_EXPIRED"])

    
    def test_user_reset_password_with_token_invalid(self):
        new_password_valid = self.serializer_data
        self.token = "sopughkldhfreoyihyfuervnyegyytnghryei-14"
        serializer = serializers.UserResetPasswordSerializer(data=new_password_valid, context={'uid': self.uid, 'token': self.token})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(str(serializer.errors['non_field_errors'][0]), res["TOKEN_IS_NOT_VALID_OR_HAS_EXPIRED"])
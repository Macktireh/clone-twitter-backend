from django.contrib.auth import get_user_model
from django.test import TestCase
from django.db.utils import IntegrityError


class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='12345')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_verified_email)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # le nom d'utilisateur est Vite pour l'option AbstractUser
            # le nom d'utilisateur n'existe pas pour l'option AbstractBaseUser
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="12345")
        with self.assertRaises(ValueError):
            User.objects.create_user(email='normal2@user.com', password='')
        with self.assertRaises(IntegrityError):
            User.objects.create_user(email='normal@user.com', password='12345')

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(email='super@user.com', password='12345')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_verified_email)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # le nom d'utilisateur est Vite pour l'option AbstractUser
            # le nom d'utilisateur n'existe pas pour l'option AbstractBaseUser
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='super-2@user.com', password='12345', is_active=False)
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='super-2@user.com', password='12345', is_verified_email=False)
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='super-2@user.com', password='12345', is_staff=False)
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='super-2@user.com', password='12345', is_superuser=False)
        with self.assertRaises(IntegrityError):
            User.objects.create_superuser(
                email='super@user.com', password='12345')
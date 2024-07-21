from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Mettre en place des objets non modifiés utilisés par toutes les méthodes de test
        User.objects.create(
            first_name="Mack", last_name="AS", email="mack@gmail.com", password="12345"
        )

    def setUp(self):
        self.user = User.objects.get(id=1)

    def test_first_name_label_and_data(self):
        field_label = self.user._meta.get_field("first_name").verbose_name
        # self.assertEqual(field_label, 'first name')
        self.assertNotEqual(field_label, "first_name")
        self.assertEqual(self.user.first_name, "Mack")

    def test_first_name_max_length(self):
        max_length = self.user._meta.get_field("first_name").max_length
        self.assertEqual(max_length, 150)

    def test_last_name_label_and_data(self):
        field_label = self.user._meta.get_field("last_name").verbose_name
        # self.assertEqual(field_label, 'last name')
        self.assertNotEqual(field_label, "last_name")
        self.assertEqual(self.user.last_name, "AS")

    def test_last_name_max_length(self):
        max_length = self.user._meta.get_field("last_name").max_length
        self.assertEqual(max_length, 150)

    def test_email_label_and_data(self):
        field_label = self.user._meta.get_field("email").verbose_name
        self.assertEqual(field_label, "email")
        self.assertEqual(self.user.email, "mack@gmail.com")

    def test_email_max_length(self):
        max_length = self.user._meta.get_field("email").max_length
        self.assertEqual(max_length, 255)

    def test_password_label_and_data(self):
        field_label = self.user._meta.get_field("password").verbose_name
        self.assertEqual(field_label, 'mot de passe')
        self.assertEqual(self.user.password, "12345")

    def test_password_max_length(self):
        max_length = self.user._meta.get_field("password").max_length
        self.assertEqual(max_length, 128)

# from django.test import TestCase
# from django.core import mail
# from django.conf import settings
# from django.template.exceptions import TemplateDoesNotExist

# from apps.authentication.models import User
# from apps.utils.email import send_email


# class SendEmailTestCase(TestCase):
    
#     def setUp(self):
#         self.user = User.objects.create(
#             first_name='Charco', 
#             last_name='AS', 
#             email='charmakepirlo@gmail.com', 
#             password='12345'
#         )
#         self.content_with_body_text = {
#             "subject": "Example email",
#             "body": "This is the content of the email",
#             "from_email": "admin@admin.com",
#             "to": [self.user.email],
#         }
#         self.content_with_body_file_html = {
#             "subject": "Example email",
#             "body": "authentication/mail/activate.html",
#             "from_email": "admin@admin.com",
#             "to": [self.user.email],
#             "token": "IJEFNRUSJEKHBEUBFER",
#             "domain": "example.com",
#         }

#     def test_send_email_body_is_text(self):
#         send_email(
#             subject=self.content_with_body_text['subject'],
#             template_name=self.content_with_body_text['body'],
#             user=self.user,
#             from_email=self.content_with_body_text['from_email']
#         )
#         # self.assertEqual(len(mail.outbox), 1)
#         email_message = mail.outbox[0]
#         self.assertEqual(email_message.subject, self.content_with_body_text['subject'])
#         self.assertEqual(email_message.body, self.content_with_body_text['body'])
#         self.assertEqual(email_message.from_email, self.content_with_body_text['from_email'])
#         self.assertEqual(email_message.to, self.content_with_body_text['to'])

#     def test_send_email_body_is_template_html(self):
#         send_email(
#             subject=self.content_with_body_file_html['subject'],
#             template_name=self.content_with_body_file_html['body'],
#             user=self.user,
#             token=self.content_with_body_file_html['token'],
#             domain=self.content_with_body_file_html['domain'],
#             from_email=self.content_with_body_file_html['from_email']
#         )
#         # self.assertEqual(len(mail.outbox), 1)
#         email_message = mail.outbox[0]
#         self.assertEqual(email_message.subject, self.content_with_body_file_html['subject'])
#         self.assertEqual(email_message.from_email, self.content_with_body_file_html['from_email'])
#         self.assertEqual(email_message.to, self.content_with_body_file_html['to'])

#     def test_send_email_body_is_template_html_not_exist(self):
#         with self.assertRaises(TemplateDoesNotExist):
#             send_email(
#                 subject=self.content_with_body_file_html['subject'],
#                 template_name='account/test.html',
#                 user=self.user,
#                 token=self.content_with_body_file_html['token'],
#                 domain=self.content_with_body_file_html['domain']
#             )

#     def test_send_email_body_is_app_not_exist(self):
#         with self.assertRaises(TemplateDoesNotExist):
#             send_email(
#                 subject=self.content_with_body_file_html['subject'],
#                 template_name='accounts/activate.html',
#                 user=self.user,
#                 token=self.content_with_body_file_html['token'],
#                 domain=self.content_with_body_file_html['domain']
#             )
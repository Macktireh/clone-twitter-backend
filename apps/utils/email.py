from threading import Thread

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import get_template
from django.utils.translation import gettext_lazy as _


def send_async_email(eamil):
    try:
        eamil.send()
    except ConnectionRefusedError:
        raise ValueError("[EMAIL SERVER] not working")

def send_email(subject, template_name, user, token=None, domain=None, from_email=settings.EMAIL_HOST_USER):
    app, ext = template_name.split('/')[0], template_name.split('.')[-1]
    if ext == 'html' and app in [app.split('.')[-1] for app in settings.LOCAL_APPS]:
        body = get_template(template_name).render({
                'user': user,
                'domain': domain or None,
                'uid': urlsafe_base64_encode(force_bytes(user.public_id)) or None,
                'token': token or None
        })
    elif ext == 'html' and app not in [app.split('.')[-1] for app in settings.LOCAL_APPS]:
        raise TemplateDoesNotExist(_('Your template does not exist'))
    else:
        body = template_name
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=from_email,
        to=[user.email]
    )
    email.content_subtype = 'html'
    Thread(target=send_async_email, args=(email,)).start()
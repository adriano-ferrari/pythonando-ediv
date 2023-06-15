from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

from .models import Users


class ActiveAccount:

    def __init__(self, user: Users):
        if not isinstance(user, Users):
            raise ValueError('User deve obrigatoriamente ser uma instância de Users.')
        self._user = user

    def _generate_url(self):
        protocol = 'http' if settings.DEBUG else 'https'
        domain = settings.DOMAIN
        uid = urlsafe_base64_encode(force_bytes(self._user.pk))
        token = default_token_generator.make_token(self._user)

        return f"{protocol}://{domain}{reverse('active_account', kwargs={'uidb4': uid, 'token': token})}"

    def active_account_send_mail(self):
        active_url = self._generate_url()
        subject = 'Ative a sua conta na EDIV...'
        mail_body = render_to_string('mails/active_account.html', {'active_url': active_url})
        email = EmailMessage(subject, mail_body, to=[self._user.email])
        if email.send():
            # TODO: Add log success
            pass
        else:
            # TODO: Add log error
            pass


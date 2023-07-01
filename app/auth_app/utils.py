from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.forms.utils import ErrorList
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.safestring import mark_safe


class SendEmailForVerify:

    def send_email_for_verify(self, user):
        current_site = get_current_site(self.request)
        context = {
            "user": user,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": token_generator.make_token(user),
            "protocol": "http",
        }
        message = render_to_string(
            template_name="auth_app/registration/verify_email.html",
            context=context,
        )
        email = EmailMessage(
            subject=f"Verify email {current_site.domain}",
            body=message,
            to=[
                user.email,
            ],
        )
        email.send()


class DivErrorList(ErrorList):
    """
    Класс для кастомного css ошибок в формах
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ""
        return mark_safe('<div class="text-danger">%s</div>' %
                         "".join(['<div class="error">%s</div>' % e for e in self]))

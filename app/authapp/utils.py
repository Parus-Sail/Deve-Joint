from django.contrib.auth.tokens import \
    default_token_generator as token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


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
            template_name="authapp/registration/verify_email.html",
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

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

# email setup
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'devejointcompany@gmail.com'
EMAIL_HOST_PASSWORD = 'rzxcfowdsrmrsnks'


class SendEmailForVerify:

    def send_email_for_verify(self):
        # current_site = get_current_site(self.request)
        current_site = 'localhost'
        context = {
            "user": 'user',
            # "domain": current_site.domain,
            "domain": 'localhost',
            "uid": urlsafe_base64_encode(force_bytes(10)),
            "token": 'my token 1231232143214',
            "protocol": "http",
        }
        message = render_to_string(
            template_name="authapp/registration/verify_email.html",
            context=context,
        )
        email = EmailMessage(
            subject=f"Verify email {'localhost'}",
            body=message,
            to=[
                'grayg@mail.ru',
            ],
        )
        email.send()


if __name__ == '__main__':
    new_email = SendEmailForVerify()
    new_email.send_email_for_verify()

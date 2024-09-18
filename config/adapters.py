from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.core.mail import send_mail
import random

from apps.authentication.models import EmailVerificationCode


class AccountAdapter(DefaultAccountAdapter):
    def send_confirmation_mail(self, request, emailconfirmation=None, signup=False, user=None):
        user = user or emailconfirmation.email_address.user

        code = EmailVerificationCode.generate_code()

        EmailVerificationCode.objects.create(user=user, code=code)

        context = {
            "user": user,
            "code": code,
            "request": request,
        }
        self.send_mail("account/email/confirmation_email", user.email, context)

    def confirm_email(self, request, email_address):
        pass

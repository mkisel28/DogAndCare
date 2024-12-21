from allauth.account.adapter import DefaultAccountAdapter

from apps.authentication.models import EmailVerificationCode


class AccountAdapter(DefaultAccountAdapter):
    def send_confirmation_mail(
        self,
        request,
        emailconfirmation=None,
        signup=False,
        user=None,
    ):
        user = user or emailconfirmation.email_address.user

        _, code = EmailVerificationCode.create_code(user=user)

        context = {
            "user": user,
            "code": code,
            "request": request,
        }
        self.send_mail("account/email/confirmation_email", user.email, context)

    def confirm_email(self, request, email_address):
        pass

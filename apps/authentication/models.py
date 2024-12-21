import random
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class EmailVerificationCode(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="email_verification_codes",
    )
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"Код подтверждения для {self.user.email}: {self.code}"

    def is_expired(self):
        expiration_period = timedelta(minutes=10)
        return timezone.now() > self.created_at + expiration_period

    def mark_as_used(self):
        self.is_used = True
        self.save()

    @staticmethod
    def generate_code():
        return f"{random.randint(100000, 999999):06d}"

    @staticmethod
    def create_code(user):
        """Creates an EmailVerificationCode instance and returns the code
        Returns:
            tuple:
            - instance of EmailVerificationCode
            - str: code
        """
        code = EmailVerificationCode.generate_code()
        return EmailVerificationCode.objects.create(user=user, code=code), code

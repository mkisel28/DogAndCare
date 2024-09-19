from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_verification_email(
    subject, plain_message, from_email, recipient_list, html_message
):
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
            html_message=html_message,
        )
    except Exception as exc:
        raise exc

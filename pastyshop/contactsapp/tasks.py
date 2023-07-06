from celery import shared_task
from django.core.mail import send_mail

from pastyshop.settings import env


@shared_task
def contacts_us(email=None, subject=None, message=None):
    """
    Task to send an e-mail notification when customers contact us.
    """
    subject, message = subject, message

    mail_sent = send_mail(subject, message, env("EMAIL_HOST_USER"), [email])
    return mail_sent

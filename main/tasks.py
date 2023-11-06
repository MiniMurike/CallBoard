from celery import shared_task
from main.celery import app
from django.core.mail import EmailMultiAlternatives


@app.task()
def send_emails_to_users(**kwargs):
    for email in kwargs['emails']:
        _email = EmailMultiAlternatives(
            subject=kwargs['subject'],
            body=kwargs['text'],
            from_email=None,
            to=[email]
        )
        _email.send()


@shared_task
def send_single_email(subject: str, text: str, email: str):
    _email = EmailMultiAlternatives(
        subject=subject,
        body=text,
        from_email=None,
        to=[email]
    )
    _email.send()


from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


@shared_task
def send_confirm_link_email(username, user_id, token, domain, email_address):
    mail_subject = 'Activate your account'
    uid = urlsafe_base64_encode(force_bytes(user_id))
    verify_link = f'http://{domain}/api/v1/auth/email-verify/{uid}/{token}/'
    message = render_to_string('authentications/verification_email.html', {'user': username, 'link': verify_link})
    send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [email_address], html_message=message)  # last


@shared_task
def send_password_reset_email(user_id, token, domain, email_address):
    mail_subject = 'Password Reset'
    uid = urlsafe_base64_encode(force_bytes(user_id))
    reset_link = f'http://{domain}/api/v1/auth/password-reset/confirm/{uid}/{token}/'
    message = render_to_string(
        'authentications/password_reset_email.html', {'link': reset_link}  # last
    )
    send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [email_address], html_message=message)

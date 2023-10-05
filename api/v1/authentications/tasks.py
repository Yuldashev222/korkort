from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string


@shared_task
def send_confirm_link_email(username, user_id, token, domain, email_address):
    mail_subject = 'Activate your account'
    uid = urlsafe_base64_encode(force_bytes(user_id))
    verify_link = f'http://{domain}/api/v1/auth/email-verify/{uid}/{token}/'
    message = render_to_string('authentications/verification_email.html', {'user': username, 'link': verify_link})
    send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [email_address], html_message=message)  # last


@shared_task
def send_password_reset_email(user_id, domain, email_address, link_type, token=None, code=None):
    mail_subject = 'Password Reset'
    link = None
    if token:
        reset_link = settings.WEB_FORGOT_PASSWORD_URL.replace('None', 'http://' + str(domain))
        uid = urlsafe_base64_encode(force_bytes(user_id))
        link = reset_link.format(uid, token)

    elif not code:
        return

    context = {'code': code, 'link': link}
    message = render_to_string('authentications/password_reset_email.html', context)  # last
    send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [email_address], html_message=message)

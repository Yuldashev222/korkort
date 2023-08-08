from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils.timezone import now


@shared_task
def delete_not_confirmed_accounts():
    get_user_model().objects.filter(date_joined__lt=now() - timedelta(minutes=30), is_verified=False).delete()

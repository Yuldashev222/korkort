from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now

from api.v1.accounts.models import CustomUser


@shared_task
def delete_not_confirmed_accounts():
    CustomUser.objects.filter(date_joined__lte=now() - timedelta(minutes=30), is_verified=False).delete()


@shared_task
def add_student_lessons(student_id):
    CustomUser.objects.filter(date_joined__lte=now() - timedelta(minutes=30), is_verified=False).delete()

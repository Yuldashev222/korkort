from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now

from api.v1.accounts.models import CustomUser
from api.v1.notifications.models import Notification
from api.v1.payments.models import Order


@shared_task
def change_student_tariff_expire_date(student_id):
    student = CustomUser.objects.get(pk=student_id)
    last_order = Order.objects.filter(student_email=student.email, is_paid=True,
                                      expire_at__gt=student.tariff_expire_date).order_by('expire_at').last()

    if last_order:
        student.tariff_expire_date = last_order.expire_at
        student.save()
        Notification.objects.create(notification_type=Notification.NOTIFICATION_TYPE[0][0], order_id=last_order.id)

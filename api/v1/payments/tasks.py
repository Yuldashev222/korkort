import os
from celery import shared_task

from api.v1.payments.models import Order
from api.v1.accounts.models import CustomUser
from api.v1.notifications.models import Notification


@shared_task
def change_student_tariff_expire_date(student_id):
    student = CustomUser.objects.get(pk=student_id)
    last_order = Order.objects.filter(student_email=student.email, is_paid=True,
                                      expire_at__gt=student.tariff_expire_date).order_by('expire_at').last()

    if last_order:
        student.tariff_expire_date = last_order.expire_at
        student.save()
        Notification.objects.create(notification_type=Notification.NOTIFICATION_TYPE[0][0], order_id=last_order.id)


@shared_task
def test_payment_webhook():
    os.system('stripe listen --forward-to https://api.lattmedkorkort.se/api/v1/payments/stripe/webhooks/')

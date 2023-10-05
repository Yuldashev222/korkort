from celery import shared_task
from django.utils.timezone import now

from api.v1.accounts.models import CustomUser
from api.v1.payments.models import Order


@shared_task
def change_student_tariff_expire_date(student_id):
    student = CustomUser.objects.get(id=student_id)
    last_order = Order.objects.filter(student=student, is_paid=True, expire_at__gt=student.tariff_expire_date).first()

    student.tariff_expire_date = last_order.expire_at if last_order else now()
    student.save()
    # delete_expire_orders()  # last

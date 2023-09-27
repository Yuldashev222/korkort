from celery import shared_task
from django.db.models import Max

from api.v1.accounts.models import CustomUser
from api.v1.payments.models import Order


@shared_task
def change_student_tariff_expire_date(student_id):
    student = CustomUser.objects.get(id=student_id)
    max_expire_at = Order.objects.filter(student=student, is_paid=True, expire_at__gt=student.tariff_expire_date
                                         ).aggregate(max_expire_at=Max('expire_at'))['max_expire_at']

    if max_expire_at:
        student.tariff_expire_date = max_expire_at
        student.save()

    # delete_expire_orders()  # last

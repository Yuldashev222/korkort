from celery import shared_task
from django.db.models import Max
from django.utils.timezone import now

from api.v1.accounts.models import CustomUser
from api.v1.lessons.models import LessonStudent
from api.v1.payments.models import Order


@shared_task
def delete_expire_orders():
    Order.expire_orders().delete()


@shared_task
def change_student_tariff_expire_date(student_id):
    try:
        student = CustomUser.objects.get(id=student_id)
    except CustomUser.DoesNotExist:
        return

    max_expire_at = Order.objects.filter(is_paid=True, expire_at__gt=now()
                                         ).aggregate(max_expire_at=Max('expire_at'))['max_expire_at']

    if max_expire_at:
        student.tariff_expire_date = max_expire_at
    else:
        student.tariff_expire_date = None
    student.save()


# @shared_task
# def add_lesson_to_students(lesson_id):
#     students = CustomUser.objects.filter(is_staff=False)
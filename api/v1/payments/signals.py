from django.db.models import Max
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from django.utils.timezone import now

from api.v1.payments.models import Order
from api.v1.payments.tasks import change_student_tariff_expire_date


@receiver(post_delete, sender=Order)
def reply_student_bonus_money(instance, *args, **kwargs):
    student = instance.student
    if student:
        if instance.is_paid:
            max_expire_at = Order.objects.filter(is_paid=True, expire_at__gt=now()
                                                 ).aggregate(max_expire_at=Max('expire_at'))['max_expire_at']
            if max_expire_at:
                instance.student.tariff_expire_date = max_expire_at
            else:
                instance.student.tariff_expire_date = None
            instance.student.save()

        elif instance.student_bonus_amount:
            student.bonus_money += instance.student_bonus_amount
            student.save()


@receiver(post_save, sender=Order)
def change_student_tariff_expire_date_on_save(instance, *args, **kwargs):
    if instance.student and instance.is_paid:
        change_student_tariff_expire_date.delay(instance.student_id)

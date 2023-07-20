from django.dispatch import receiver
from django.db.models.signals import post_delete

from api.v1.payments.models import Order


@receiver(post_delete, sender=Order)
def reply_student_bonus_price(instance, *args, **kwargs):
    if not instance.is_paid:
        if instance.student and instance.student_bonus_price:
            instance.student.bonus_price += instance.student_bonus_price
            instance.student.save()

from django.dispatch import receiver
from django.db.models.signals import post_delete

from api.v1.payments.models import Order


@receiver(post_delete, sender=Order)
def reply_student_bonus_money(instance, *args, **kwargs):
    student = instance.student
    if not instance.is_paid and student and instance.student_bonus_amount:
        student.bonus_money += instance.student_bonus_amount
        student.save()

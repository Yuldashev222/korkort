from django.dispatch import receiver
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete

from api.v1.swish.models import SwishCard, MinBonusMoney


@receiver(post_save, sender=SwishCard)
def change_student_bonus_money(instance, *args, **kwargs):
    if instance.is_paid and not instance.is_purchased and instance.student:
        student_bonus_money = instance.student.bonus_money
        if student_bonus_money >= instance.purchased_price:
            instance.student.bonus_money -= instance.purchased_price
        else:
            instance.student.bonus_money = 0
        instance.student.save()
        instance.is_purchased = True
        instance.save()


@receiver([post_save, post_delete], sender=MinBonusMoney)
def update_tariffs_cache(*args, **kwargs):
    cache.clear()

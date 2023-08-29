from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from api.v1.tariffs.models import Tariff
from api.v1.discounts.models import StudentDiscount, TariffDiscount


@receiver([post_save, post_delete], sender=StudentDiscount)
def update_tariff_discount(*args, **kwargs):
    StudentDiscount.set_redis()
    for tariff in Tariff.objects.filter(student_discount=True):
        tariff.save()


@receiver([post_delete, post_save], sender=TariffDiscount)
def update_tariff_discount(*args, **kwargs):
    TariffDiscount.set_redis()
    for tariff in Tariff.objects.filter(tariff_discount=True):
        tariff.save()

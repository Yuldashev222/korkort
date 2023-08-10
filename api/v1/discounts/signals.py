from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from api.v1.tariffs.models import Tariff
from api.v1.discounts.models import StudentDiscount, TariffDiscount


@receiver(post_save, sender=StudentDiscount)
def update_tariff_discount(instance, *args, **kwargs):
    StudentDiscount.set_redis()
    for tariff in Tariff.objects.all():
        tariff.save()


@receiver(post_delete, sender=StudentDiscount)
def update_tariff_discount(instance, *args, **kwargs):
    StudentDiscount.set_redis()
    Tariff.objects.update(student_discount=False)


@receiver(post_save, sender=TariffDiscount)
def update_tariff_discount(instance, *args, **kwargs):
    for tariff in instance.tariff_set.all():
        tariff.save()


@receiver(post_delete, sender=TariffDiscount)
def update_tariff_discount(instance, *args, **kwargs):
    for tariff in instance.tariff_set.all():
        tariff.save()

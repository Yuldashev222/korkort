import os

from django.core.cache import cache
from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save

from .models import TariffInfo, Tariff
from ..discounts.models import TariffDiscount, StudentDiscount


@receiver(post_delete, sender=TariffInfo)
def delete_tariff_image(instance, *args, **kwargs):
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)


@receiver(pre_save, sender=TariffInfo)
def update_tariff_image(instance, *args, **kwargs):
    if instance.pk:
        tariff = TariffInfo.objects.get(pk=instance.pk)
        if tariff.image and tariff.image != instance.image:
            if os.path.isfile(tariff.image.path):
                os.remove(tariff.image.path)


@receiver(pre_save, sender=Tariff)
def update_discounts(instance, *args, **kwargs):
    for field in ['tariff_discount', 'student_discount']:
        if getattr(instance, field):
            discount = cache.get(field)
            if not discount:
                if field == 'tariff_discount':
                    TariffDiscount.set_redis()
                else:
                    StudentDiscount.set_redis()
                discount = cache.get(field)

            if not discount or discount.get('valid_to') and discount['valid_to'] <= now().date():
                setattr(instance, field + '_amount', 0)
                setattr(instance, field, False)
            else:
                if discount['is_percent']:
                    value = instance.price * discount['discount_value'] / 100
                    setattr(instance, field + '_amount', value)
                    setattr(instance, field + '_amount', round(value, 1))
                else:
                    setattr(instance, field + '_amount', discount['discount_value'])

        else:
            setattr(instance, field + '_amount', 0)

from django.dispatch import receiver
from django.core.cache import cache
from django.db.models.signals import pre_save, post_save

from .models import Tariff
from api.v1.discounts.models import TariffDiscount, StudentDiscount


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

            # if not discount or discount.get('valid_to') and discount['valid_to'] <= now().date():
            if not discount:
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


@receiver(post_save, sender=Tariff)
def update_tariffs_cache(instance, *args, **kwargs):
    instance.set_redis()

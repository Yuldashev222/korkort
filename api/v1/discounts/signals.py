from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save

from api.v1.general.utils import delete_object_file_post_delete, delete_object_file_pre_save
from api.v1.tariffs.models import Tariff
from api.v1.discounts.models import StudentDiscount, TariffDiscount


@receiver(post_delete, sender=TariffDiscount)
def delete_image(instance, *args, **kwargs):
    delete_object_file_post_delete(instance, 'image')


@receiver(pre_save, sender=TariffDiscount)
def delete_image(instance, *args, **kwargs):
    delete_object_file_pre_save(TariffDiscount, instance, 'image')


@receiver([post_save, post_delete], sender=StudentDiscount)  # last
def update_tariff_discount(*args, **kwargs):
    for tariff in Tariff.objects.filter(student_discount=True):
        tariff.save()

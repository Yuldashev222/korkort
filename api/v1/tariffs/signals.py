import os

from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save

from .models import TariffInfo


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

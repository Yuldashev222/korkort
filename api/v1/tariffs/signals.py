import os

from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save

from .models import Tariff


@receiver(post_delete, sender=Tariff)
def delete_tariff_image(instance, *args, **kwargs):
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)


@receiver(pre_save, sender=Tariff)
def update_tariff_image(instance, *args, **kwargs):
    if instance.pk:
        tariff = Tariff.objects.get(pk=instance.pk)
        if tariff.image and tariff.image != instance.image:
            if os.path.isfile(tariff.image.path):
                os.remove(tariff.image.path)

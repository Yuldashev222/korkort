from django.dispatch import receiver
from api.v1.general.utils import delete_object_file_post_delete, delete_object_file_pre_save
from django.db.models.signals import post_delete, pre_save

from api.v1.discounts.models import TariffDiscount


@receiver(post_delete, sender=TariffDiscount)
def delete_image(instance, *args, **kwargs):
    delete_object_file_post_delete(instance, 'image')


@receiver(pre_save, sender=TariffDiscount)
def delete_image(instance, *args, **kwargs):
    delete_object_file_pre_save(TariffDiscount, instance, 'image')

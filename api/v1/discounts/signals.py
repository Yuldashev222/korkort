from django.dispatch import receiver
from api.v1.general.utils import delete_object_file_post_delete, delete_object_file_pre_save
from django.db.models.signals import post_delete, pre_save, post_save

from api.v1.discounts.models import TariffDiscount
from api.v1.notifications.models import Notification


@receiver(post_delete, sender=TariffDiscount)
def delete_image(instance, *args, **kwargs):
    delete_object_file_post_delete(instance, 'image')


@receiver(pre_save, sender=TariffDiscount)
def delete_image(instance, *args, **kwargs):
    delete_object_file_pre_save(TariffDiscount, instance, 'image')


@receiver(post_save, sender=TariffDiscount)
def create_notification(instance, created, *args, **kwargs):
    if created:
        Notification.objects.create(notification_type=Notification.NOTIFICATION_TYPE[4][0],
                                    tariff_discount_id=instance.pk)

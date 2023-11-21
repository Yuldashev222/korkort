from django.dispatch import receiver
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete

from api.v1.swish.models import MinBonusMoney, SwishCard, CalledStudentAndSwishTransaction


@receiver([post_save, post_delete], sender=MinBonusMoney)
def update_tariffs_cache(instance, *args, **kwargs):
    cache.clear()
    instance.set_redis()


@receiver(post_save, sender=SwishCard)
def create_transaction(instance, *args, **kwargs):
    CalledStudentAndSwishTransaction.objects.get_or_create(swish_card_id=instance.pk)

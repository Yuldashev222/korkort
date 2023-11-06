from django.dispatch import receiver
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete

from api.v1.swish.models import MinBonusMoney


@receiver([post_save, post_delete], sender=MinBonusMoney)
def update_tariffs_cache(instance, *args, **kwargs):
    cache.clear()
    instance.set_redis()

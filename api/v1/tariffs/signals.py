from django.dispatch import receiver
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete

from api.v1.tariffs.models import Tariff


@receiver([post_save, post_delete], sender=Tariff)
def update_tariffs_cache(*args, **kwargs):
    cache.clear()

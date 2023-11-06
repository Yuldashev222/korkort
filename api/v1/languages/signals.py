from django.dispatch import receiver
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete

from api.v1.languages.models import Language


@receiver([post_save, post_delete], sender=Language)
def update_cache(*args, **kwargs):
    Language.set_redis()
    cache.clear()

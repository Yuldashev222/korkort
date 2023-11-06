from django.dispatch import receiver
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete

from api.v1.levels.models import Level, LevelDetail


@receiver([post_save, post_delete], sender=Level)
def clear_cache(*args, **kwargs):
    cache.clear()


@receiver([post_save, post_delete], sender=LevelDetail)
def clear_cache(*args, **kwargs):
    cache.clear()

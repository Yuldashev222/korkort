from django.dispatch import receiver
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete

from api.v1.todos.models import TodoDetail, Todo


@receiver([post_save, post_delete], sender=TodoDetail)
def update_tariffs_cache(*args, **kwargs):
    cache.clear()


@receiver([post_save, post_delete], sender=Todo)
def update_tariffs_cache(*args, **kwargs):
    cache.clear()

from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from api.v1.levels.models import Level


@receiver([post_save, post_delete], sender=Level)
def update_cache(instance, *args, **kwargs):
    Level.set_redis()

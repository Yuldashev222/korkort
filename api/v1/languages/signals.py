from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from api.v1.languages.models import Language


@receiver([post_save, post_delete], sender=Language)
def update_cache(instance, *args, **kwargs):
    Language.set_redis()

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from api.v1.balls.models import TestBall


@receiver([post_save, post_delete], sender=TestBall)
def update_cache(*args, **kwargs):
    TestBall.set_redis()

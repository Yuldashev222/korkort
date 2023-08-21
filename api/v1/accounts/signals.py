from django.db.models.signals import post_save
from django.dispatch import receiver

from api.v1.accounts.tasks import add_student_lessons
from api.v1.accounts.models import CustomUser


@receiver(post_save, sender=CustomUser)
def add_lessons(instance, created, *args, **kwargs):
    if created and not instance.is_staff:
        add_student_lessons.delay(instance.id)

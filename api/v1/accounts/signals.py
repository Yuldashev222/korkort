from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

from api.v1.accounts.tasks import create_objects_for_student
from api.v1.accounts.models import CustomUser


@receiver(pre_save, sender=CustomUser)
def add_lessons(instance, *args, **kwargs):
    if not instance.pk:
        if instance.is_staff:
            instance.user_code = instance.email
            instance.is_verified = True

        else:
            instance.user_code = instance.generate_unique_user_code


@receiver(post_save, sender=CustomUser)
def add_lessons(instance, created, *args, **kwargs):
    if created:
        create_objects_for_student.delay(instance.id)

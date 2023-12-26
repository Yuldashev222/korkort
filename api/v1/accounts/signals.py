from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import pre_save

from api.v1.accounts.models import CustomUser
from api.v1.general.services import normalize_text


@receiver(pre_save, sender=CustomUser)
def change_fields_pre_save(instance, *args, **kwargs):
    instance.name = normalize_text(instance.name)[0]
    if not instance.is_staff:
        instance.ball = instance.correct_answers * settings.TEST_BALL + instance.completed_lessons * settings.LESSON_BALL
        instance.level_id = len([counts for counts in settings.LEVELS if instance.ball >= counts])
        instance.bonus_money = round(instance.bonus_money, 1)

        if not instance.pk:
            instance.user_code = instance.generate_unique_user_code

    elif not instance.pk:
        instance.user_code = instance.email
        instance.is_verified = True

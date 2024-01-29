from datetime import timedelta

from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.utils.timezone import now

from api.v1.accounts.models import CustomUser
from api.v1.general.services import normalize_text
from api.v1.notifications.models import Notification


@receiver(pre_save, sender=CustomUser)
def change_fields_pre_save(instance, *args, **kwargs):
    instance.name = normalize_text(instance.name)[0]
    if not instance.is_staff:
        instance.ball = instance.correct_answers * settings.TEST_BALL + instance.completed_lessons * settings.LESSON_BALL

        balls = list(settings.LEVELS)
        old_level_id = instance.level_id
        instance.level_id = len([ball for ball in balls if instance.ball >= ball])
        if instance.level_id < len(settings.LEVELS):
            instance.level_percent = int(instance.ball / balls[instance.level_id] * 100)
        else:
            instance.level_percent = 100

        instance.bonus_money = round(instance.bonus_money, 1)

        if not instance.pk:
            instance.user_code = instance.generate_unique_user_code
            instance.tariff_expire_date = now().date() - timedelta(days=1)
        elif instance.level_id != old_level_id:
            Notification.objects.create(notification_type=Notification.NOTIFICATION_TYPE[1][0], student_id=instance.pk)

    elif not instance.pk:
        instance.user_code = instance.email
        instance.is_verified = True

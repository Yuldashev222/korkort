from datetime import timedelta

from django.dispatch import receiver
from django.utils.timezone import now
from django.db.models.signals import post_save

from api.v1.accounts.tasks import add_student_lessons
from api.v1.lessons.models import LessonStudentStatisticsByDay
from api.v1.accounts.models import CustomUser


@receiver(post_save, sender=CustomUser)
def add_lessons(instance, created, *args, **kwargs):
    if created and not instance.is_staff:
        add_student_lessons.delay(instance.id)
        today_date = now().date()
        objs = [
            LessonStudentStatisticsByDay(student=instance, date=today_date - timedelta(days=i))
            for i in [0, 1, 2, 3, 4, 5, 6]
        ]
        LessonStudentStatisticsByDay.objects.bulk_create(objs)

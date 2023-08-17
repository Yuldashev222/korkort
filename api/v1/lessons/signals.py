from django.dispatch import receiver
from django.db.models import Sum
from django.db.models.signals import post_save, post_delete

from api.v1.lessons.models import Lesson


@receiver([post_save, post_delete], sender=Lesson)
def update_chapter_time_on_save(instance, *args, **kwargs):
    if instance.chapter:
        chapter = instance.chapter
        time_in_minute = Lesson.objects.filter(chapter=chapter).aggregate(time=Sum('lesson_time'))['time']
        if not time_in_minute:
            chapter.chapter_hour = 0
            chapter.chapter_minute = 0
        else:
            chapter.chapter_hour = time_in_minute // 60
            chapter.chapter_minute = time_in_minute % 60
        chapter.save()

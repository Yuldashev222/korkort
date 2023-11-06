from django.core.cache import cache
from django.dispatch import receiver
from django.db.models import Sum, Count
from django.db.models.signals import post_save, post_delete, pre_save

from api.v1.general.utils import delete_object_file_post_delete, delete_object_file_pre_save
from api.v1.lessons.models import Lesson, LessonStudent
from api.v1.accounts.models import CustomUser
from api.v1.chapters.models import ChapterStudent


def update_chapter_time(instance, *args, **kwargs):  # last
    if instance.chapter:
        chapter = instance.chapter
        data = Lesson.objects.filter(chapter_id=chapter.pk).aggregate(time=Sum('lesson_time'), cnt=Count('pk'))
        time_in_minute, lessons = data.get('time'), data.get('cnt')

        if not time_in_minute:
            chapter.chapter_hour, chapter.chapter_minute = 0, 0
        else:
            chapter.chapter_hour, chapter.chapter_minute = divmod(time_in_minute, 60)

        chapter.lessons = lessons if lessons else 0
        chapter.save()
    cache.clear()
    Lesson.set_redis()


@receiver(post_delete, sender=Lesson)
def delete_image(instance, *args, **kwargs):
    delete_object_file_post_delete(instance, 'image')
    update_chapter_time(instance, *args, **kwargs)


@receiver(pre_save, sender=Lesson)
def delete_image(instance, *args, **kwargs):
    delete_object_file_pre_save(Lesson, instance, 'image')


@receiver(post_save, sender=Lesson)
def add_to_student_on_create(instance, created, *args, **kwargs):
    if created:
        student_ids = CustomUser.objects.filter(is_staff=False).values_list('pk', flat=True)
        objs = (LessonStudent(student_id=student_id, lesson_id=instance.pk) for student_id in student_ids)
        LessonStudent.objects.bulk_create(objs)

    update_chapter_time(instance, *args, **kwargs)


@receiver(post_save, sender=LessonStudent)
def update_student_ball(instance, *args, **kwargs):
    if instance.is_completed and instance.student and instance.lesson.chapter:
        completed_lessons = LessonStudent.objects.filter(student_id=instance.student_id, is_completed=True,
                                                         lesson__chapter_id=instance.lesson.chapter_id).count()
        obj, _ = ChapterStudent.objects.get_or_create(chapter_id=instance.lesson.chapter_id,
                                                      student_id=instance.student_id)
        if obj.completed_lessons != completed_lessons:
            obj.completed_lessons = completed_lessons
            obj.save()

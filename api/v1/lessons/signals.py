import shutil

from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models import Sum, Count
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete, pre_save

from api.v1.general.utils import delete_object_file_post_delete, delete_object_file_pre_save
from api.v1.lessons.models import Lesson, LessonStudent, LessonDetail
from api.v1.chapters.models import ChapterStudent
from api.v1.lessons.services import extract_m3u8_zip_file, get_m3u8_directory_location
from api.v1.lessons.validators import validate_m3u8_zip_file
from api.v1.notifications.models import Notification


def update_chapter_time(instance, *args, **kwargs):  # last
    if instance.chapter:
        chapter = instance.chapter
        data = Lesson.objects.filter(chapter_id=chapter.pk).aggregate(time=Sum('lesson_time', default=0),
                                                                      cnt=Count('pk'))
        time_in_minute, lessons = data['time'], data['cnt']
        chapter.chapter_hour, chapter.chapter_minute = (0, 0) if not time_in_minute else divmod(time_in_minute, 60)
        chapter.lessons = lessons
        chapter.save()
    cache.clear()  # last
    Lesson.set_redis()  # last


@receiver(post_delete, sender=Lesson)
def delete_image(instance, *args, **kwargs):
    delete_object_file_post_delete(instance, 'image')
    update_chapter_time(instance, *args, **kwargs)


@receiver(pre_save, sender=Lesson)
def delete_image(instance, *args, **kwargs):
    delete_object_file_pre_save(Lesson, instance, 'image')


@receiver(post_save, sender=Lesson)
def add_to_student_on_create(instance, *args, **kwargs):
    update_chapter_time(instance, *args, **kwargs)


@receiver(post_save, sender=LessonStudent)
def update_student_chapter_completed_lessons(instance, *args, **kwargs):
    if instance.is_completed:  # Warning
        completed_lessons = LessonStudent.objects.filter(student_id=instance.student_id, is_completed=True,
                                                         lesson__chapter_id=instance.lesson.chapter_id).count()
        chapter_student, _ = ChapterStudent.objects.get_or_create(chapter_id=instance.lesson.chapter_id,
                                                                  student_id=instance.student_id)
        if chapter_student.completed_lessons != completed_lessons:
            chapter_student.completed_lessons = completed_lessons
            chapter_student.save()
        else:
            Notification.objects.create(notification_type=Notification.NOTIFICATION_TYPE[2][0],
                                        chapter_id=chapter_student.chapter_id,
                                        student_id=chapter_student.student_id)


@receiver(post_delete, sender=LessonDetail)
def delete_zip_file(instance, *args, **kwargs):
    try:
        shutil.rmtree(get_m3u8_directory_location(lesson_detail=instance))
    except FileNotFoundError:
        pass
    cache.clear()  # last


@receiver(post_save, sender=LessonDetail)
def update_lesson_detail_cache(instance, *args, **kwargs):
    try:
        validate_m3u8_zip_file(m3u8_zip_file_url=instance.m3u8_zip.path)
        extract_m3u8_zip_file(lesson_detail=instance)
    except ValidationError:
        instance.delete()
    except FileNotFoundError:
        print(2)
        pass

    cache.clear()  # last

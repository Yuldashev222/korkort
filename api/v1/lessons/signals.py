from datetime import timedelta

from django.dispatch import receiver
from django.db.models import Sum, Count
from django.db.models.signals import post_save, post_delete, pre_save
from django.utils.timezone import now

from api.v1.accounts.models import CustomUser
from api.v1.chapters.models import ChapterStudent
from api.v1.general.utils import delete_object_file_post_delete, delete_object_file_pre_save
from api.v1.lessons.models import Lesson, LessonStudent


@receiver(post_delete, sender=Lesson)
def delete_image(instance, *args, **kwargs):
    delete_object_file_post_delete(instance, 'image')
    delete_object_file_post_delete(instance, 'video_en')
    delete_object_file_post_delete(instance, 'video_swe')
    delete_object_file_post_delete(instance, 'video_e_swe')
    update_chapter_time(instance, *args, **kwargs)


@receiver(pre_save, sender=Lesson)
def delete_image(instance, *args, **kwargs):
    try:
        delete_object_file_pre_save(Lesson, instance, 'image')
        delete_object_file_pre_save(Lesson, instance, 'video_en')
        delete_object_file_pre_save(Lesson, instance, 'video_swe')
        delete_object_file_pre_save(Lesson, instance, 'video_e_swe')
    except Lesson.DoesNotExist:
        pass


def update_chapter_time(instance, *args, **kwargs):  # last
    if instance.chapter:
        chapter = instance.chapter
        data = Lesson.objects.filter(chapter=chapter).aggregate(time=Sum('lesson_time'),
                                                                cnt=Count('id'))
        time_in_minute, lessons = data.get('time'), data.get('cnt')
        if not time_in_minute:
            chapter.chapter_hour = 0
            chapter.chapter_minute = 0
        else:
            chapter.chapter_hour = time_in_minute // 60
            chapter.chapter_minute = time_in_minute % 60

        chapter.lessons = lessons if lessons else 0
        chapter.save()
    Lesson.set_redis()


@receiver(post_save, sender=Lesson)
def add_to_student_on_create(instance, created, *args, **kwargs):
    if created:
        student_ids = CustomUser.objects.filter(is_staff=False).values_list('id', flat=True)
        objs = (LessonStudent(student_id=student_id, lesson_id=instance.id) for student_id in student_ids)
        LessonStudent.objects.bulk_create(objs)

    update_chapter_time(instance, *args, **kwargs)


@receiver(post_save, sender=LessonStudent)
def update_student_ball(instance, *args, **kwargs):
    if instance.student:
        completed_lessons = LessonStudent.objects.filter(student=instance.student, is_completed=True,
                                                         lesson__chapter=instance.lesson.chapter).count()
        obj, _ = ChapterStudent.objects.get_or_create(chapter=instance.lesson.chapter, student=instance.student)
        obj.completed_lessons = completed_lessons
        obj.save()

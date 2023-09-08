from django.dispatch import receiver
from django.db.models import Sum, Count, Q
from django.db.models.signals import post_save, post_delete

from api.v1.accounts.models import CustomUser
from api.v1.chapters.models import ChapterStudent
from api.v1.lessons.models import Lesson, LessonStudent, LessonStudentStatistics, LessonStudentStatisticsByDay


@receiver([post_save, post_delete], sender=Lesson)
def update_chapter_time(instance, *args, **kwargs):
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


@receiver([post_save, post_delete], sender=LessonStudentStatistics)
def change_student_lesson_view_statistics(instance, *args, **kwargs):
    if instance.student:
        obj, _ = LessonStudentStatisticsByDay.objects.get_or_create(date=instance.viewed_date, student=instance.student)
        cnt = LessonStudentStatistics.objects.filter(student=instance.student, viewed_date=instance.viewed_date
                                                     ).aggregate(cnt=Count('id'))['cnt']
        obj.count = cnt if cnt else 0
        obj.save()


@receiver(post_save, sender=LessonStudentStatisticsByDay)
def change_student_lesson_view_statistics(instance, *args, **kwargs):
    if instance.student:
        expire_objs = LessonStudentStatisticsByDay.objects.filter(student=instance.student
                                                                  ).values_list('id', flat=True)[7:]
        LessonStudentStatisticsByDay.objects.filter(student=instance.student, id__in=expire_objs).delete()


@receiver(post_save, sender=Lesson)
def add_to_student_on_create(instance, created, *args, **kwargs):
    if created:
        student_ids = CustomUser.objects.filter(is_staff=False).values_list('id', flat=True)
        objs = (LessonStudent(student_id=student_id, lesson_id=instance.id) for student_id in student_ids)
        LessonStudent.objects.bulk_create(objs)


@receiver([post_save, post_delete], sender=LessonStudent)
def update_student_ball(instance, *args, **kwargs):
    completed_lessons = LessonStudent.objects.filter(student=instance.student, is_completed=True,
                                                     lesson__chapter=instance.lesson.chapter).count()
    obj, _ = ChapterStudent.objects.get_or_create(chapter=instance.lesson.chapter, student=instance.student)
    obj.completed_lessons = completed_lessons
    obj.save()

from django.dispatch import receiver
from django.db.models import Sum, Count
from django.db.models.signals import post_save, post_delete

from api.v1.accounts.models import CustomUser
from api.v1.lessons.models import Lesson, LessonStudent, LessonStudentStatistics, LessonStudentStatisticsByDay


@receiver([post_save, post_delete], sender=Lesson)
def update_chapter_time(instance, *args, **kwargs):
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


@receiver([post_save, post_delete], sender=LessonStudentStatistics)
def change_student_lesson_view_statistics(instance, *args, **kwargs):
    if instance.student:
        obj, _ = LessonStudentStatisticsByDay.objects.get_or_create(date=instance.viewed_date, student=instance.student)
        cnt = LessonStudentStatistics.objects.filter(student=instance.student, viewed_date=instance.viewed_date
                                                     ).aggregate(cnt=Count('id'))['cnt']
        obj.count = cnt if cnt else 0
        obj.save()


@receiver(post_save, sender=Lesson)
def add_to_student_on_create(instance, created, *args, **kwargs):
    if created:
        student_ids = CustomUser.objects.filter(is_staff=False).values_list('id', flat=True)
        objs = (LessonStudent(student_id=student_id, lesson_id=instance.id) for student_id in student_ids)
        LessonStudent.objects.bulk_create(objs)

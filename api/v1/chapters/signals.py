from django.dispatch import receiver
from django.db.models import Sum
from django.db.models.signals import post_save, pre_save, post_delete

from api.v1.lessons.models import LessonStudent
from api.v1.accounts.models import CustomUser
from api.v1.chapters.models import Chapter, ChapterStudent


@receiver(post_save, sender=Chapter)
def add_chapter_to_all_students(instance, created, *args, **kwargs):
    if created:
        students = CustomUser.objects.filter(is_staff=False)
        objs = [ChapterStudent(student=student, chapter=instance) for student in students]
        ChapterStudent.objects.bulk_create(objs)


@receiver(pre_save, sender=ChapterStudent)
def add_chapter_to_all_students(instance, *args, **kwargs):
    obj = LessonStudent.objects.filter(student=instance.student, lesson__chapter=instance.chapter,
                                       is_completed=True).last()
    if not obj:
        obj = LessonStudent.objects.filter(student=instance.student, lesson__chapter=instance.chapter).first()
    instance.last_lesson = obj if obj else None

    old_obj = ChapterStudent.objects.filter(student=instance.student, chapter=instance.chapter,
                                            chapter__ordering_number__lt=instance.chapter.ordering_number).last()

    if not old_obj:
        instance.is_open = True
    else:
        instance.is_open = old_obj.completed_lessons == old_obj.chapter.lessons


@receiver([post_save, post_delete], sender=ChapterStudent)
def update_student_completed_lessons(instance, *args, **kwargs):
    completed_lessons = ChapterStudent.objects.filter(student=instance.student
                                                      ).aggregate(cnt=Sum('completed_lessons'))['cnt']
    if completed_lessons:
        instance.student.completed_lessons = completed_lessons
    else:
        instance.student.completed_lessons = 0
    instance.student.save()

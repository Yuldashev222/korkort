from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from api.v1.accounts.models import CustomUser
from api.v1.chapters.models import Chapter, ChapterStudent
from api.v1.lessons.models import LessonStudent


@receiver(post_save, sender=Chapter)
def add_chapter_to_all_students(instance, created, *args, **kwargs):
    if created:
        students = CustomUser.objects.filter(is_staff=False)
        objs = [ChapterStudent(student=student, chapter=instance) for student in students]
        ChapterStudent.objects.bulk_create(objs)


@receiver(pre_save, sender=ChapterStudent)
def add_chapter_to_all_students(instance, *args, **kwargs):
    obj = LessonStudent.objects.filter(student=instance.student, lesson__chapter=instance.chapter, is_completed=True
                                       ).order_by('lesson__ordering_number').last()
    if not obj:
        obj = LessonStudent.objects.filter(student=instance.student, lesson__chapter=instance.chapter
                                           ).order_by('lesson__ordering_number').first()
    instance.last_lesson = obj if obj else None

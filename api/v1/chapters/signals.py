from django.dispatch import receiver
from django.db.models import Sum
from django.db.models.signals import post_save, pre_save, post_delete

from api.v1.general.utils import delete_object_file_post_delete, delete_object_file_pre_save
from api.v1.chapters.models import Chapter, ChapterStudent


@receiver(post_delete, sender=Chapter)
def delete_image(instance, *args, **kwargs):
    delete_object_file_post_delete(instance, 'image')


@receiver(pre_save, sender=Chapter)
def delete_image(instance, *args, **kwargs):
    delete_object_file_pre_save(Chapter, instance, 'image')


@receiver(post_save, sender=ChapterStudent)
def update_student_completed_lessons(instance, *args, **kwargs):
    student = instance.student
    if student:
        completed_lessons = ChapterStudent.objects.filter(student_id=student.pk
                                                          ).aggregate(amount=Sum('completed_lessons'))['amount']
        if student.completed_lessons != completed_lessons:
            student.completed_lessons = completed_lessons
            student.save()

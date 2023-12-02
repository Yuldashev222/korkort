from django.dispatch import receiver
from django.db.models.signals import post_save

from api.v1.exams.models import CategoryExamStudent, StudentLastExamResult


@receiver(post_save, sender=CategoryExamStudent)
def delete_redundant_exams(instance, *args, **kwargs):
    expire_objs = CategoryExamStudent.objects.filter(category_id=instance.category_id, student_id=instance.student_id
                                                     ).values_list('pk', flat=True).order_by('-pk')[10:]
    CategoryExamStudent.objects.filter(id__in=expire_objs).delete()


@receiver(post_save, sender=StudentLastExamResult)
def delete_the_excess(instance, *args, **kwargs):
    if instance.student:
        expire_objs = StudentLastExamResult.objects.filter(student_id=instance.student.pk
                                                           ).values_list('pk', flat=True).order_by('-pk')[10:]
        StudentLastExamResult.objects.filter(pk__in=expire_objs).delete()

from django.dispatch import receiver
from django.db.models import Avg
from django.db.models.signals import post_save

from api.v1.exams.models import CategoryExamStudent


@receiver(post_save, sender=CategoryExamStudent)
def delete_redundant_exams(instance, *args, **kwargs):
    if instance.student and instance.result:
        expire_objs = CategoryExamStudent.objects.filter(student=instance.student, result=instance.result
                                                         ).values_list('id', flat=True)[10:]
        CategoryExamStudent.objects.filter(student=instance.student, result=instance.result,
                                           id__in=expire_objs).delete()

        objs = CategoryExamStudent.objects.filter(result=instance.result, student=instance.student)

        avg_percent = objs.aggregate(avg_percent=Avg('percent'))['avg_percent']
        instance.result.percent = avg_percent
        instance.result.save()

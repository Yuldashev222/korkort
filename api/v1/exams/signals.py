from django.db.models.signals import post_save
from django.dispatch import receiver

from api.v1.exams.models import CategoryExamStudent


@receiver(post_save, sender=CategoryExamStudent)
def delete_redundant_exams(instance, *args, **kwargs):
    expire_objs = CategoryExamStudent.objects.filter(student=instance.student, category=instance.category
                                                     ).values_list('id', flat=True)[10:]
    CategoryExamStudent.objects.filter(student=instance.student, category=instance.category,
                                       id__in=expire_objs).delete()

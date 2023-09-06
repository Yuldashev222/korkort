from django.db.models import Count, Sum
from django.dispatch import receiver
from django.db.models.signals import post_save

from api.v1.exams.models import CategoryExamStudent, CategoryExamStudentResult


@receiver(post_save, sender=CategoryExamStudent)
def delete_redundant_exams(instance, *args, **kwargs):
    expire_objs = CategoryExamStudent.objects.filter(student=instance.student, category=instance.category
                                                     ).values_list('id', flat=True)[10:]
    CategoryExamStudent.objects.filter(student=instance.student, category=instance.category,
                                       id__in=expire_objs).delete()

    objs = CategoryExamStudent.objects.filter(category=instance.category, student=instance.student)

    percent_query = objs.aggregate(all_percent=Sum('percent'), cnt=Count('id'))
    if percent_query['cnt'] > 0:
        obj, _ = CategoryExamStudentResult.objects.get_or_create(category=instance.category, student=instance.student)
        obj.percent = int(percent_query['all_percent'] / percent_query['cnt'])
    else:
        obj, _ = CategoryExamStudentResult.objects.get_or_create(category=instance.category, student=instance.student)
        obj.percent = 0
    obj.exams.set(objs)
    obj.save()

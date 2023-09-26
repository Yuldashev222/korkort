from django.dispatch import receiver
from django.db.models import Avg, Sum
from django.db.models.signals import post_save

from api.v1.exams.models import CategoryExamStudent, StudentLastExamResult


@receiver(post_save, sender=CategoryExamStudent)
def delete_redundant_exams(instance, *args, **kwargs):
    if instance.result:
        expire_objs = CategoryExamStudent.objects.filter(result=instance.result).values_list('id', flat=True)[10:]
        CategoryExamStudent.objects.filter(result=instance.result, id__in=expire_objs).delete()

        objs = CategoryExamStudent.objects.filter(result=instance.result)
        avg_percent = objs.aggregate(avg_percent=Avg('percent'))['avg_percent']
        instance.result.percent = avg_percent
        instance.result.save()


@receiver(post_save, sender=StudentLastExamResult)
def delete_the_excess(instance, *args, **kwargs):
    if instance.student:
        expire_objs = StudentLastExamResult.objects.filter(student=instance.student).values_list('id', flat=True)[10:]
        StudentLastExamResult.objects.filter(student=instance.student, id__in=expire_objs).delete()

        data = StudentLastExamResult.objects.filter(student=instance.student).aggregate(questions=Sum('questions'),
                                                                                        answers=Sum('wrong_answers'))

        all_questions = data['questions']
        all_correct_answers = all_questions - data['answers']
        instance.student.last_exams_result = int(all_correct_answers / all_questions * 100)
        instance.student.save()

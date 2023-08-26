from django.db.models import Count
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from api.v1.questions.models import Question, QuestionStudentLastResult


@receiver([post_save, post_delete], sender=Question)
def update_question_count(*args, **kwargs):
    Question.set_redis()


@receiver(post_save, sender=QuestionStudentLastResult)
def delete_the_excess(instance, *args, **kwargs):
    expire_objs = QuestionStudentLastResult.objects.filter(student=instance.student
                                                           ).order_by('-id').values_list('id', flat=True)[10:]
    QuestionStudentLastResult.objects.filter(student=instance.student, id__in=expire_objs).delete()
    data = QuestionStudentLastResult.objects.aggregate(questions=Count('questions'), answers=Count('correct_answers'))
    instance.student.last_exams_result = int(data.get('answers') / data.get('questions') * 100)
    instance.student.save()

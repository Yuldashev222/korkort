from django.db.models import Count
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from api.v1.questions.models import ExamQuestion, QuestionStudentLastResult


@receiver([post_save, post_delete], sender=ExamQuestion)
def update_exam_question_count(*args, **kwargs):
    ExamQuestion.set_redis()


@receiver(post_save, sender=QuestionStudentLastResult)
def delete_the_excess(instance, *args, **kwargs):
    QuestionStudentLastResult.objects.filter(student=instance.student).order_by('-id')[10:].delete()
    data = QuestionStudentLastResult.objects.aggregate(questions=Count('questions'), answers=Count('correct_answers'))
    instance.student.last_exams_result = int(data.get('answers') / data.get('questions') * 100)
    instance.student.save()

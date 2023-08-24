from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from api.v1.questions.models import ExamQuestion, LessonQuestion


@receiver([post_save, post_delete], sender=ExamQuestion)
def update_exam_question_count(*args, **kwargs):
    ExamQuestion.set_redis()


@receiver([post_save, post_delete], sender=LessonQuestion)
def update_lesson_question_count(*args, **kwargs):
    LessonQuestion.set_redis()

from datetime import timedelta

from celery import shared_task
from django.core.cache import cache
from django.utils.timezone import now

from api.v1.accounts.models import CustomUser
from api.v1.lessons.models import Lesson, LessonStudent
from api.v1.questions.models import ExamQuestion, LessonQuestion, WrongQuestionStudentAnswer


@shared_task
def delete_not_confirmed_accounts():
    CustomUser.objects.filter(date_joined__lte=now() - timedelta(minutes=30), is_verified=False).delete()


@shared_task
def add_student_lessons(student_id):
    first_chapter_lesson_ids = Lesson.objects.values_list('id', flat=True)
    objs = (LessonStudent(lesson_id=lesson_id, student_id=student_id) for lesson_id in first_chapter_lesson_ids)
    LessonStudent.objects.bulk_create(objs)  # last


@shared_task
def update_student_correct_answers(student_id):
    all_questions_count = cache.get('all_questions_count')
    if not all_questions_count:
        ExamQuestion.set_redis()  # last
        all_questions_count = cache.get('all_questions_count')
    if all_questions_count:
        student = CustomUser.objects.get(id=student_id)
        wrong_answers_count = WrongQuestionStudentAnswer.objects.filter(student=student).count()
        student.correct_answers = all_questions_count - wrong_answers_count
        student.save()

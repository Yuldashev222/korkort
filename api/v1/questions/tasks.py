from uuid import uuid4

from celery import shared_task

from api.v1.accounts.tasks import update_student_correct_answers
from api.v1.lessons.models import Lesson
from api.v1.questions.models import Question, StudentWrongAnswer, Category


@shared_task
def update_student_wrong_answers_in_lesson_test(student_id, lesson_id, wrong_question_ids):
    StudentWrongAnswer.objects.filter(question__lesson_id=lesson_id, student_id=student_id).delete()
    if wrong_question_ids:
        questions = Question.objects.filter(id__in=wrong_question_ids)
        objs = [StudentWrongAnswer(question=question, student_id=student_id) for question in questions]
        StudentWrongAnswer.objects.bulk_create(objs)

    update_student_correct_answers(student_id)


@shared_task
def update_student_wrong_answers_in_exam_test(student_id, wrong_question_ids, correct_question_ids):
    StudentWrongAnswer.objects.filter(question_id__in=correct_question_ids + wrong_question_ids,
                                      student_id=student_id).delete()
    if wrong_question_ids:
        questions = Question.objects.filter(id__in=wrong_question_ids)
        objs = [StudentWrongAnswer(question=question, student_id=student_id) for question in questions]
        StudentWrongAnswer.objects.bulk_create(objs)

    update_student_correct_answers(student_id)

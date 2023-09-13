from celery import shared_task

from api.v1.accounts.services import update_student_correct_answers
from api.v1.questions.models import StudentWrongAnswer, StudentCorrectAnswer


def bulk_create_answers(model_class, question_ids, student_id):
    if question_ids:
        objs = [model_class(question_id=question_id, student_id=student_id) for question_id in question_ids]
        model_class.objects.bulk_create(objs)


@shared_task
def delete_student_correct_and_wrong_fields(model_class, question_ids, student_id):
    model_class.objects.filter(question_id__in=question_ids, student_id=student_id).delete()


@shared_task
def update_student_wrong_answers_in_lesson_exam(student_id, lesson_id, wrong_question_ids, correct_question_ids):
    StudentWrongAnswer.objects.filter(question__lesson_id=lesson_id, student_id=student_id).delete()

    delete_student_correct_and_wrong_fields(StudentCorrectAnswer, wrong_question_ids + correct_question_ids, student_id)
    bulk_create_answers(StudentCorrectAnswer, correct_question_ids, student_id)
    bulk_create_answers(StudentWrongAnswer, wrong_question_ids, student_id)
    update_student_correct_answers(student_id)


@shared_task
def update_student_wrong_answers_in_exam(student_id, wrong_question_ids, correct_question_ids):
    delete_student_correct_and_wrong_fields(StudentWrongAnswer, wrong_question_ids + correct_question_ids, student_id)

    delete_student_correct_and_wrong_fields(StudentCorrectAnswer, wrong_question_ids + correct_question_ids, student_id)
    bulk_create_answers(StudentCorrectAnswer, correct_question_ids, student_id)
    bulk_create_answers(StudentWrongAnswer, wrong_question_ids, student_id)
    update_student_correct_answers(student_id)

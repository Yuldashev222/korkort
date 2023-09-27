from celery import shared_task

from api.v1.accounts.services import update_student_correct_answers
from api.v1.questions.models import StudentWrongAnswer, StudentCorrectAnswer


def bulk_create_answers(model_class, question_ids, student_id):
    if question_ids:
        objs = [model_class(question_id=question_id, student_id=student_id) for question_id in question_ids]
        model_class.objects.bulk_create(objs)


@shared_task
def update_student_wrong_answers(student_id, wrong_question_ids, correct_question_ids, lesson_id=None):
    StudentCorrectAnswer.objects.filter(question_id__in=wrong_question_ids + correct_question_ids, student_id=student_id
                                        ).delete()

    if lesson_id is not None:
        StudentWrongAnswer.objects.filter(question__lesson_id=lesson_id, student_id=student_id).delete()
    else:
        StudentWrongAnswer.objects.filter(question_id__in=wrong_question_ids + correct_question_ids,
                                          student_id=student_id).delete()

    bulk_create_answers(StudentCorrectAnswer, correct_question_ids, student_id)
    bulk_create_answers(StudentWrongAnswer, wrong_question_ids, student_id)

    update_student_correct_answers(student_id)

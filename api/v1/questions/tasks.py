from celery import shared_task

from api.v1.accounts.tasks import update_student_correct_answers

from api.v1.questions.models import Question, WrongQuestionStudentAnswer


@shared_task
def update_student_wrong_answers(student_id, lesson_id, correct_answers_ids, for_lesson):
    WrongQuestionStudentAnswer.objects.filter(question_id__in=correct_answers_ids, student_id=student_id).delete()

    for question in Question.objects.filter(for_lesson=for_lesson, lesson_id=lesson_id).exclude(
            id__in=correct_answers_ids):
        WrongQuestionStudentAnswer.objects.get_or_create(question=question, student_id=student_id)

    update_student_correct_answers(student_id)

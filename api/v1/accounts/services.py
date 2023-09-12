from api.v1.accounts.models import CustomUser
from api.v1.questions.models import Question, StudentCorrectAnswer


def update_student_correct_answers(student_id):
    all_questions_count = Question.get_all_questions_count()
    student = CustomUser.objects.get(id=student_id)
    cnt = StudentCorrectAnswer.objects.filter(student=student).count()
    student.correct_answers = cnt if all_questions_count > 0 else 0
    student.save()

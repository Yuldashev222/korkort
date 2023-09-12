from api.v1.accounts.models import CustomUser
from api.v1.questions.models import StudentCorrectAnswer


def update_student_correct_answers(student_id):
    student = CustomUser.objects.get(id=student_id)
    student.correct_answers = StudentCorrectAnswer.objects.filter(student=student).count()
    student.save()

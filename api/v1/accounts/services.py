from datetime import timedelta
from django.utils.timezone import now

from api.v1.accounts.models import CustomUser
from api.v1.questions.models import StudentCorrectAnswer


def update_student_correct_answers(student_id):
    student = CustomUser.objects.get(id=student_id)
    student.correct_answers = StudentCorrectAnswer.objects.filter(student=student).count()
    student.save()


def delete_not_confirmed_accounts():
    CustomUser.objects.filter(date_joined__lte=now() - timedelta(hours=1), is_staff=False, is_verified=False).delete()

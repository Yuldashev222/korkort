from django.conf import settings

from api.v1.questions.models import Question
from api.v1.exams.views.wrongs import WrongQuestionsExamAPIView
from api.v1.exams.views.general import ExamAnswerAPIView
from api.v1.exams.serializers.saved import SavedQuestionsExamAnswerSerializer


class SavedQuestionsExamAPIView(WrongQuestionsExamAPIView):
    def get_queryset(self, my_questions=False, difficulty_level=None, counts=settings.MIN_QUESTIONS):
        student = self.request.user
        queryset = Question.objects.filter(studentsavedquestion__isnull=False)  # last

        if difficulty_level:
            queryset = queryset.filter(difficulty_level=difficulty_level)

        if my_questions:
            queryset = queryset.filter(studentsavedquestion__student_id=student.pk)
        else:
            queryset = queryset.exclude(studentsavedquestion__student_id=student.pk)

        return list(queryset.order_by('?')[:counts])


class SavedQuestionsExamAnswerAPIView(ExamAnswerAPIView):
    serializer_class = SavedQuestionsExamAnswerSerializer

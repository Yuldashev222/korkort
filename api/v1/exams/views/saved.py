from api.v1.questions.models import Question
from api.v1.exams.views.wrongs import WrongQuestionsExamAPIView
from api.v1.exams.views.general import ExamAnswerAPIView
from api.v1.exams.serializers.saved import SavedQuestionsExamAnswerSerializer


class SavedQuestionsExamAPIView(WrongQuestionsExamAPIView):
    queryset = Question.objects.filter(studentsavedquestion__isnull=False).order_by('?')


class SavedQuestionsExamAnswerAPIView(ExamAnswerAPIView):
    serializer_class = SavedQuestionsExamAnswerSerializer

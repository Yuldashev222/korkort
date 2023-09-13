from api.v1.exams.filters import SavedQuestionsExamFilter
from api.v1.questions.models import StudentSavedQuestion
from api.v1.exams.views.wrongs import WrongQuestionsExamAPIView
from api.v1.exams.views.general import ExamAnswerAPIView
from api.v1.exams.serializers.saved import SavedQuestionsExamAnswerSerializer


class SavedQuestionsExamAnswerAPIView(ExamAnswerAPIView):
    serializer_class = SavedQuestionsExamAnswerSerializer


class SavedQuestionsExamAPIView(WrongQuestionsExamAPIView):
    filterset_class = SavedQuestionsExamFilter
    queryset = StudentSavedQuestion.objects.order_by('?')

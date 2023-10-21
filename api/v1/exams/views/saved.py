from api.v1.questions.models import Question
from api.v1.exams.views.wrongs import WrongQuestionsExamAPIView
from api.v1.exams.views.general import ExamAnswerAPIView
from api.v1.exams.serializers.saved import SavedQuestionsExamAnswerSerializer


class SavedQuestionsExamAPIView(WrongQuestionsExamAPIView):

    def get_queryset(self):
        queryset = Question.objects.filter(studentsavedquestion__isnull=False).order_by('?')
        my_questions = self.request.query_params.get('my_questions')

        if my_questions == 'true':
            queryset = queryset.filter(studentsavedquestion__student_id=self.request.user.id)

        return queryset


class SavedQuestionsExamAnswerAPIView(ExamAnswerAPIView):
    serializer_class = SavedQuestionsExamAnswerSerializer

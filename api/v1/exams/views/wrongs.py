from django.conf import settings
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from api.v1.exams.filters import WrongQuestionsExamFilter
from api.v1.exams.serializers.wrongs import WrongQuestionsExamSerializer, WrongQuestionsExamAnswerSerializer
from api.v1.questions.models import StudentWrongAnswer, StudentSavedQuestion
from api.v1.exams.views.general import ExamAnswerAPIView
from api.v1.accounts.permissions import IsStudent


class WrongQuestionsExamAnswerAPIView(ExamAnswerAPIView):
    serializer_class = WrongQuestionsExamAnswerSerializer


class WrongQuestionsExamAPIView(ListAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = WrongQuestionsExamSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = WrongQuestionsExamFilter

    queryset = StudentWrongAnswer.objects.select_related('question__category').order_by('?')
    
    def get_serializer_context(self):
        student_saved_question_ids = list(StudentSavedQuestion.objects.filter(
            student=self.request.user).values_list('question_id', flat=True).order_by('question_id'))
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'student_saved_question_ids': student_saved_question_ids
        }

    def filter_queryset(self, queryset):
        my_questions = self.request.query_params.get('my_questions')
        counts = self.request.query_params.get('counts')
        if my_questions == 'true':
            queryset = queryset.filter(student=self.request.user)

        if counts:
            try:
                counts = int(counts)
                if counts <= settings.MAX_QUESTIONS:
                    queryset = queryset[:counts]
            except (ValueError, TypeError):
                raise ValidationError({'counts': 'not valid'})
        else:
            queryset = queryset[:settings.MAX_QUESTIONS]
        return queryset

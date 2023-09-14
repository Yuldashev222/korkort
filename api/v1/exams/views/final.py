from random import sample
from django.conf import settings
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from api.v1.questions.models import Question, StudentSavedQuestion
from api.v1.accounts.permissions import IsStudent
from api.v1.exams.serializers.general import QuestionExamSerializer


class FinalExamAPIView(ListAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = QuestionExamSerializer

    def get_serializer_context(self):
        student_saved_question_ids = list(StudentSavedQuestion.objects.filter(
            student=self.request.user).values_list('question_id', flat=True).order_by('question_id'))
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'student_saved_question_ids': student_saved_question_ids
        }

    def get_queryset(self):
        random_questions = sample(Question.get_question_ids(), settings.MAX_QUESTIONS)
        return Question.objects.filter(id__in=random_questions).select_related('category'
                                                                               ).prefetch_related('variant_set')

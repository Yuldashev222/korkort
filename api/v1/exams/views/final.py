from random import sample
from django.conf import settings
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from api.v1.questions.models import Question
from api.v1.accounts.permissions import IsStudent
from api.v1.exams.serializers.general import QuestionExamSerializer


class FinalExamAPIView(ListAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = QuestionExamSerializer

    def get_queryset(self):
        random_questions = sample(Question.get_question_ids(), settings.MAX_QUESTIONS)
        return Question.objects.filter(id__in=random_questions).select_related('category'
                                                                               ).prefetch_related('variant_set')

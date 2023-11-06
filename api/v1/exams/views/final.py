from django.conf import settings
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.utils.translation import get_language
from rest_framework.permissions import IsAuthenticated

from api.v1.questions.models import Question, StudentSavedQuestion, QuestionDetail
from api.v1.accounts.permissions import IsStudent
from api.v1.questions.serializers.questions import QuestionSerializer


class FinalExamAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsStudent)  # last
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.filter(questiondetail__language_id=get_language()
                                       ).order_by('?')[:settings.FINAL_QUESTIONS]

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())

        question_text_list = QuestionDetail.objects.filter(question__in=queryset, language_id=get_language()
                                                           ).values('question_id',
                                                                    'text',
                                                                    'correct_variant',
                                                                    'variant2',
                                                                    'variant3',
                                                                    'variant4',
                                                                    'answer'
                                                                    ).order_by('question_id')

        student_saved_question_list = StudentSavedQuestion.objects.filter(
            student_id=self.request.user.pk, question__in=queryset).values('question_id').order_by('question_id')

        ctx = self.get_serializer_context()
        ctx['student_saved_question_list'] = student_saved_question_list
        ctx['question_text_list'] = question_text_list
        return Response(self.serializer_class(queryset, many=True, context=ctx).data)

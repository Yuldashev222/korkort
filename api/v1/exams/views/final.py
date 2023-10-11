from random import sample
from django.conf import settings
from django.utils.translation import get_language
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.v1.questions.models import Question, StudentSavedQuestion, QuestionDetail, Variant, CategoryDetail
from api.v1.accounts.permissions import IsStudent
from api.v1.exams.serializers.general import QuestionExamSerializer


class FinalExamAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = QuestionExamSerializer

    def get_queryset(self):
        random_questions = sample(Question.get_question_ids(), settings.FINAL_QUESTIONS)
        return Question.objects.filter(id__in=random_questions)

    def get(self, request, *args, **kwargs):
        questions_queryset = list(self.get_queryset())

        question_text_list = QuestionDetail.objects.filter(question__in=questions_queryset,
                                                           language=get_language()).values('question', 'text', 'answer'
                                                                                           ).order_by('question_id')

        variant_list = Variant.objects.filter(language=get_language(), question__in=questions_queryset
                                              ).values('question', 'text', 'is_correct')

        student_saved_question_list = StudentSavedQuestion.objects.filter(
            student=self.request.user, question__in=questions_queryset).values('question').order_by('question_id')

        category_name_list = CategoryDetail.objects.filter(
            language=get_language(), category__question__in=questions_queryset).values('category', 'name').order_by(
            'category_id')

        ctx = self.get_serializer_context()
        ctx['student_saved_question_list'] = student_saved_question_list
        ctx['category_name_list'] = category_name_list
        ctx['question_text_list'] = question_text_list
        ctx['variant_list'] = variant_list
        return Response(QuestionExamSerializer(questions_queryset, many=True, context=ctx).data)

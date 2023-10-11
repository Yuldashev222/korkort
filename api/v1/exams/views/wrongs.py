from django.conf import settings
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.utils.translation import get_language
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from api.v1.exams.filters import QuestionFilter
from api.v1.exams.serializers.general import QuestionExamSerializer
from api.v1.questions.models import CategoryDetail, Question, QuestionDetail, Variant, StudentSavedQuestion
from api.v1.exams.views.general import ExamAnswerAPIView
from api.v1.accounts.permissions import IsStudent
from api.v1.exams.serializers.wrongs import WrongQuestionsExamAnswerSerializer


class WrongQuestionsExamAnswerAPIView(ExamAnswerAPIView):
    serializer_class = WrongQuestionsExamAnswerSerializer


class WrongQuestionsExamAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = QuestionExamSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = QuestionFilter

    queryset = Question.objects.filter(studentwronganswer__isnull=False).order_by('?')

    def get(self, request, *args, **kwargs):
        questions_queryset = list(self.filter_queryset(self.get_queryset()))

        category_name_list = CategoryDetail.objects.filter(category__question__in=questions_queryset,
                                                           language=get_language()).values('category', 'name').order_by(
            'category_id')

        question_text_list = QuestionDetail.objects.filter(question__in=questions_queryset,
                                                           language=get_language()).values('question', 'text', 'answer'
                                                                                           ).order_by('question_id')

        variant_list = Variant.objects.filter(language=get_language(), question__in=questions_queryset
                                              ).values('question', 'text', 'is_correct')

        student_saved_question_list = StudentSavedQuestion.objects.filter(
            student=self.request.user, question__in=questions_queryset).values('question').order_by('question_id')

        category_name_list = CategoryDetail.objects.filter(
            language=get_language(), category__question__in=questions_queryset).values('category', 'name'
                                                                                       ).order_by('category_id')

        ctx = self.get_serializer_context()
        ctx['student_saved_question_list'] = student_saved_question_list
        ctx['category_name_list'] = category_name_list
        ctx['question_text_list'] = question_text_list
        ctx['variant_list'] = variant_list
        serializer = self.get_serializer(questions_queryset, many=True, context=ctx)
        return Response(serializer.data)

    def filter_queryset(self, queryset):
        my_questions = self.request.query_params.get('my_questions')
        counts = self.request.query_params.get('counts')
        difficulty_level = self.request.query_params.get('difficulty_level')

        if my_questions == 'true':
            queryset = queryset.filter(student=self.request.user)

        if difficulty_level:
            try:
                difficulty_level = int(difficulty_level)
            except ValueError:
                raise ValidationError({'difficulty_level': 'not valid'})

            if difficulty_level not in [1, 2, 3]:
                raise ValidationError({'difficulty_level': 'not valid'})

            queryset = queryset.filter(question__difficulty_level=difficulty_level)

        if counts:
            try:
                counts = int(counts)
            except ValueError:
                raise ValidationError({'counts': 'not valid'})

            if counts > settings.MAX_QUESTIONS or counts < settings.MIN_QUESTIONS:
                raise ValidationError({'counts': 'not valid'})

            queryset = queryset[:counts]
        else:
            queryset = queryset[:settings.MIN_QUESTIONS]
        return queryset

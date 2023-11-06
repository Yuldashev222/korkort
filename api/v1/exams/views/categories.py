from django.conf import settings
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.utils.translation import get_language
from rest_framework.permissions import IsAuthenticated

from api.v1.questions.models import Question, StudentSavedQuestion, QuestionDetail
from api.v1.exams.views.general import ExamAnswerAPIView
from api.v1.accounts.permissions import IsStudent
from api.v1.exams.serializers.categories import (CategoryExamAnswerSerializer, CategoryExamCreateSerializer,
                                                 CategoryMixExamCreateSerializer, CategoryMixExamAnswerSerializer)
from api.v1.questions.serializers.questions import QuestionSerializer


class CategoryExamAnswerAPIView(ExamAnswerAPIView):
    serializer_class = CategoryExamAnswerSerializer


class CategoryMixExamAnswerAPIView(ExamAnswerAPIView):
    serializer_class = CategoryMixExamAnswerSerializer


class CategoryExamAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsStudent)  # last
    serializer_class = CategoryExamCreateSerializer

    def get_queryset(self, category_id_list=None, difficulty_level=None, counts=settings.MIN_QUESTIONS):
        queryset = Question.objects.filter(questiondetail__language_id=get_language())

        if category_id_list:
            queryset = queryset.filter(category_id__in=category_id_list)

        if difficulty_level:
            queryset = queryset.filter(difficulty_level=difficulty_level)

        return queryset.order_by('?')[:counts]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        counts = serializer.validated_data['counts']
        category_id = serializer.validated_data['category_id']
        difficulty_level = serializer.validated_data.get('difficulty_level')

        queryset = list(self.get_queryset([category_id], difficulty_level, counts))

        question_text_list = QuestionDetail.objects.filter(question__in=queryset, language_id=get_language()
                                                           ).values('pk', 'question_id', 'text',
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
        questions = QuestionSerializer(queryset, many=True, context=ctx).data
        return Response(questions, status=HTTP_201_CREATED)


class CategoryMixExamAPIView(CategoryExamAPIView):
    serializer_class = CategoryMixExamCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        counts = serializer.validated_data['counts']
        difficulty_level = serializer.validated_data.get('difficulty_level')
        category_id_list = serializer.validated_data.get('category_id_list')

        queryset = list(self.get_queryset(category_id_list=category_id_list, difficulty_level=difficulty_level,
                                          counts=counts))

        question_text_list = QuestionDetail.objects.filter(question__in=queryset, language_id=get_language()
                                                           ).values('question_id', 'text',
                                                                    'correct_variant',
                                                                    'variant2',
                                                                    'variant3',
                                                                    'variant4',
                                                                    'answer'
                                                                    ).order_by('question_id')

        student_saved_question_list = StudentSavedQuestion.objects.filter(
            student_id=self.request.user.pk, question__in=queryset).values('question_id').order_by('question_id')

        ctx = self.get_serializer_context()
        ctx['question_text_list'] = question_text_list
        ctx['student_saved_question_list'] = student_saved_question_list

        questions = QuestionSerializer(queryset, many=True, context=ctx).data
        return Response(questions, status=HTTP_200_OK)

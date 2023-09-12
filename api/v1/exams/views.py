from random import sample
from django.conf import settings
from rest_framework.status import HTTP_201_CREATED
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from api.v1.exams.models import CategoryExamStudentResult
from api.v1.exams.filters import WrongQuestionsExamFilter
from api.v1.questions.models import Question, StudentWrongAnswer
from api.v1.exams.serializers import CategoryExamStudentResultSerializer, WrongQuestionsExamSerializer
from api.v1.accounts.permissions import IsStudent
from api.v1.questions.serializers.exams import (QuestionExamSerializer,
                                                CategoryExamAnswerSerializer,
                                                QuestionExamCreateSerializer)


class ExamAnswerAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsStudent)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=HTTP_201_CREATED)


class CategoryExamAnswerAPIView(ExamAnswerAPIView):
    serializer_class = CategoryExamAnswerSerializer


class CategoryExamAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = QuestionExamCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        obj = serializer.obj
        filter_data = {'category_id': request.data['category_id']}
        if obj.difficulty_level:
            filter_data['difficulty_level'] = obj.difficulty_level

        # question_ids = sample(Question.get_question_ids(), obj.questions)
        questions_queryset = Question.objects.filter(
            **filter_data).prefetch_related('variant_set', 'studentsavedquestion_set').order_by('?')[:obj.questions]
        # id__in=question_ids, **filter_data).prefetch_related('lesson__lessonstudent_set', 'variant_set')

        questions = QuestionExamSerializer(questions_queryset, many=True, context={'request': request}).data
        return Response({'exam_id': obj.id, 'questions': questions}, status=HTTP_201_CREATED)


class ExamStudentResult(GenericAPIView):
    permission_classes = (IsAuthenticated, IsStudent)

    def get(self, request, *args, **kwargs):
        student = self.request.user
        category_exam_query = CategoryExamStudentResult.objects.filter(
            student=student).prefetch_related('categoryexamstudent_set')
        category_exams = CategoryExamStudentResultSerializer(category_exam_query, many=True,
                                                             context={'request': request}).data
        data = {'category_exams': category_exams}
        return Response(data)


class WrongQuestionsExamAPIView(ListAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = WrongQuestionsExamSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = WrongQuestionsExamFilter

    queryset = StudentWrongAnswer.objects.select_related('question', 'question__lesson'
                                                         ).prefetch_related('question__variant_set')

    def filter_queryset(self, queryset):
        my_questions = self.request.query_params.get('my_questions')
        counts = self.request.query_params.get('counts')
        if my_questions == 'true':
            queryset = queryset.filter(student=self.request.user)

        try:
            counts = int(counts)
            if counts <= settings.MAX_QUESTIONS:
                queryset = queryset[:counts]
        except (ValueError, TypeError):
            pass
        return queryset

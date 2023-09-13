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
                                                QuestionExamCreateSerializer, WrongQuestionsExamAnswerSerializer)


class ExamAnswerAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsStudent)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=HTTP_201_CREATED)


class CategoryExamAnswerAPIView(ExamAnswerAPIView):
    serializer_class = CategoryExamAnswerSerializer


class WrongQuestionsExamAnswerAPIView(ExamAnswerAPIView):
    serializer_class = WrongQuestionsExamAnswerSerializer


class CategoryExamAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = QuestionExamCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        obj = serializer.obj
        category_id = request.data['category_id']
        difficulty_level = request.data.get('difficulty_level')
        filter_data = {'category_id': category_id}
        if difficulty_level:
            filter_data['difficulty_level'] = difficulty_level

        questions_queryset = Question.objects.filter(**filter_data).prefetch_related('variant_set'
                                                                                     ).order_by('?')[:obj.questions]

        questions = QuestionExamSerializer(questions_queryset, many=True, context={'request': request}).data
        return Response({'exam_id': obj.id, 'questions': questions}, status=HTTP_201_CREATED)


class ExamStudentResult(GenericAPIView):
    permission_classes = (IsAuthenticated, IsStudent)

    def get(self, request, *args, **kwargs):
        student = self.request.user
        category_exam_query = CategoryExamStudentResult.objects.filter(student=student
                                                                       ).prefetch_related('categoryexamstudent_set')
        category_exams = CategoryExamStudentResultSerializer(category_exam_query, many=True,
                                                             context={'request': request}).data
        data = {'category_exams': category_exams}
        return Response(data)


class WrongQuestionsExamAPIView(ListAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = WrongQuestionsExamSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = WrongQuestionsExamFilter

    queryset = StudentWrongAnswer.objects.select_related('question__lesson')

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

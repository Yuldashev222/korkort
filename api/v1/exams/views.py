from rest_framework.status import HTTP_201_CREATED
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from api.v1.exams.models import CategoryExamStudent
from api.v1.questions.models import Question
from api.v1.exams.serializers import ExamStudentCategorySerializer
from api.v1.accounts.permissions import IsStudent
from api.v1.questions.serializers.exams import (
    QuestionExamSerializer,
    CategoryExamAnswerSerializer,
    QuestionExamCreateSerializer
)


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
        data = serializer.data

        filter_data = {'category_id': data['category']}
        if data.get('difficulty_level'):
            filter_data['difficulty_level'] = data.get('difficulty_level')

        questions_queryset = Question.objects.filter(**filter_data).prefetch_related('variant_set',
                                                                                     'lesson__lessonstudent_set'
                                                                                     ).order_by('?')[:data['questions']]
        questions = QuestionExamSerializer(questions_queryset, many=True, context={'request': request}).data

        return Response({'exam_id': data['id'], 'questions': questions}, status=HTTP_201_CREATED)


class ExamStudentResult(GenericAPIView):
    permission_classes = (IsAuthenticated, IsStudent)

    def get(self, request, *args, **kwargs):
        student = self.request.user
        category_exam_query = CategoryExamStudent.objects.filter(student=student).select_related('category')
        category_exams = ExamStudentCategorySerializer(category_exam_query, many=True,
                                                       context={'request': request}).data
        data = {
            'category_exams': category_exams
        }
        return Response(data)

from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from api.v1.questions.models import Question, StudentSavedQuestion
from api.v1.exams.views.general import ExamAnswerAPIView
from api.v1.accounts.permissions import IsStudent
from api.v1.exams.serializers.general import QuestionExamSerializer
from api.v1.exams.serializers.categories import (CategoryExamAnswerSerializer, CategoryExamCreateSerializer,
                                                 CategoryMixExamCreateSerializer, CategoryMixExamAnswerSerializer)


class CategoryExamAnswerAPIView(ExamAnswerAPIView):
    serializer_class = CategoryExamAnswerSerializer


class CategoryMixExamAnswerAPIView(ExamAnswerAPIView):
    serializer_class = CategoryMixExamAnswerSerializer


class CategoryExamAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = CategoryExamCreateSerializer

    def get_serializer_context(self):
        student_saved_question_ids = list(StudentSavedQuestion.objects.filter(
            student=self.request.user).values_list('question_id', flat=True).order_by('question_id'))
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'student_saved_question_ids': student_saved_question_ids
        }

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        obj = serializer.obj
        filter_data = {'category_id': int(request.data['category_id'])}

        difficulty_level = request.data.get('difficulty_level')
        if difficulty_level:
            filter_data['difficulty_level'] = int(difficulty_level)

        questions_queryset = Question.objects.filter(
            **filter_data).select_related('category').prefetch_related('variant_set').order_by('?')[:obj.questions]

        questions = QuestionExamSerializer(questions_queryset, many=True, context=self.get_serializer_context()).data
        return Response({'exam_id': obj.id, 'questions': questions}, status=HTTP_201_CREATED)


class CategoryMixExamAPIView(CategoryExamAPIView):
    serializer_class = CategoryMixExamCreateSerializer
    queryset = Question.objects.select_related('category').prefetch_related('variant_set')

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        questions = serializer.validated_data['questions']
        difficulty_level = serializer.validated_data['difficulty_level']
        if difficulty_level:
            questions_queryset = self.queryset.filter(difficulty_level=difficulty_level)
        else:
            questions_queryset = self.queryset
        questions_queryset = questions_queryset.order_by('?')[:questions]
        questions = QuestionExamSerializer(questions_queryset, many=True, context=self.get_serializer_context()).data
        return Response(questions, status=HTTP_200_OK)

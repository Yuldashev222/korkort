from django.utils.translation import get_language
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from api.v1.questions.models import Question, StudentSavedQuestion, CategoryDetail, QuestionDetail, Variant
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

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        obj = serializer.obj
        filter_data = {'category_id': int(request.data['category_id'])}

        difficulty_level = request.data.get('difficulty_level')
        if difficulty_level:
            filter_data['difficulty_level'] = int(difficulty_level)

        questions_queryset = list(Question.objects.filter(**filter_data).order_by('?')[:obj.questions])

        question_text_list = QuestionDetail.objects.filter(question__in=questions_queryset,
                                                           language=get_language()).values('question', 'text', 'answer'
                                                                                           ).order_by('question_id')

        variant_list = Variant.objects.filter(language=get_language(), question__in=questions_queryset
                                              ).values('question', 'text', 'is_correct')

        student_saved_question_list = StudentSavedQuestion.objects.filter(
            student=self.request.user, question__in=questions_queryset).values('question').order_by('question_id')

        ctx = self.get_serializer_context()
        ctx['student_saved_question_list'] = student_saved_question_list
        ctx['category_name_list'] = []
        ctx['question_text_list'] = question_text_list
        ctx['variant_list'] = variant_list

        questions = QuestionExamSerializer(questions_queryset, many=True, context=ctx).data
        return Response({'exam_id': obj.id, 'questions': questions}, status=HTTP_201_CREATED)


class CategoryMixExamAPIView(CategoryExamAPIView):
    serializer_class = CategoryMixExamCreateSerializer
    queryset = Question.objects.all()

    def post(self, request, *args, **kwargs):
        queryset = self.queryset
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        questions = serializer.validated_data['questions']
        difficulty_level = serializer.validated_data['difficulty_level']
        category_ids = serializer.validated_data.get('category_ids')

        if category_ids:
            category_ids = list(map(lambda obj: obj['pk'], category_ids))
            queryset = queryset.filter(category_id__in=category_ids)

        if difficulty_level:
            queryset = queryset.filter(difficulty_level=difficulty_level)

        queryset = list(queryset.order_by('?')[:questions])

        question_text_list = QuestionDetail.objects.filter(question__in=queryset, language=get_language()
                                                           ).values('question', 'text', 'answer'
                                                                    ).order_by('question_id')

        variant_list = Variant.objects.filter(language=get_language(), question__in=queryset
                                              ).values('question', 'text', 'is_correct')

        student_saved_question_list = StudentSavedQuestion.objects.filter(
            student=self.request.user, question__in=queryset).values('question').order_by('question_id')

        category_name_list = CategoryDetail.objects.filter(
            language=get_language(), category__question__in=queryset).values('category', 'name').order_by('category_id')

        ctx = self.get_serializer_context()
        ctx['question_text_list'] = question_text_list
        ctx['variant_list'] = variant_list
        ctx['student_saved_question_list'] = student_saved_question_list
        ctx['category_name_list'] = category_name_list

        questions = QuestionExamSerializer(queryset, many=True, context=ctx).data
        return Response(questions, status=HTTP_200_OK)

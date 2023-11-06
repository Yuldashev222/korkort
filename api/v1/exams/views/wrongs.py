from django.conf import settings
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.utils.translation import get_language
from rest_framework.permissions import IsAuthenticated

from api.v1.questions.models import Question, QuestionDetail, StudentSavedQuestion
from api.v1.exams.views.general import ExamAnswerAPIView
from api.v1.accounts.permissions import IsStudent
from api.v1.exams.serializers.wrongs import WrongQuestionsExamAnswerSerializer, WrongQuestionsExamSerializer
from api.v1.questions.serializers.questions import QuestionSerializer


class WrongQuestionsExamAnswerAPIView(ExamAnswerAPIView):
    serializer_class = WrongQuestionsExamAnswerSerializer


class WrongQuestionsExamAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsStudent)  # last
    serializer_class = WrongQuestionsExamSerializer

    def get_queryset(self, my_questions=False, difficulty_level=None, counts=settings.MIN_QUESTIONS):
        student = self.request.user
        queryset = Question.objects.filter(studentwronganswer__isnull=False, questiondetail__language_id=get_language())

        if difficulty_level:
            queryset = queryset.filter(difficulty_level=difficulty_level)

        if my_questions:
            queryset = queryset.filter(studentwronganswer__student_id=student.pk)
        else:
            queryset = queryset.exclude(studentwronganswer__student_id=student.pk)

        return queryset.order_by('?')[:counts]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        my_questions = serializer.validated_data['my_questions']
        difficulty_level = serializer.validated_data.get('difficulty_level')
        counts = serializer.validated_data['counts']
        student = self.request.user

        queryset = list(self.get_queryset(my_questions, difficulty_level, counts))

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
            student_id=student.pk, question__in=queryset).values('question_id').order_by('question_id')

        ctx = self.get_serializer_context()
        ctx['student_saved_question_list'] = student_saved_question_list
        ctx['question_text_list'] = question_text_list
        serializer = QuestionSerializer(queryset, many=True, context=ctx)
        return Response(serializer.data)

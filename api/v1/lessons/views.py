from datetime import timedelta

from django.db.models import Count
from django.utils.timezone import now
from django.utils.translation import get_language
from rest_framework.generics import GenericAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_201_CREATED

from api.v1.lessons.tasks import change_student_lesson_view_statistics
from api.v1.lessons.models import LessonStudent, StudentLessonViewStatistics, Lesson
from api.v1.exams.views.general import ExamAnswerAPIView
from api.v1.lessons.permissions import OldLessonCompleted, IsOpenOrPurchased, OldLessonCompletedForQuestions
from api.v1.lessons.serializers import (LessonRetrieveSerializer, StudentLessonViewStatisticsSerializer,
                                        LessonAnswerSerializer)
from api.v1.questions.models import StudentSavedQuestion, Question, QuestionDetail, CategoryDetail, Variant
from api.v1.accounts.permissions import IsStudent
from api.v1.questions.serializers.questions import QuestionSerializer


class LessonAnswerAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsStudent, OldLessonCompletedForQuestions, IsOpenOrPurchased)
    serializer_class = LessonAnswerSerializer

    def post(self, request, *args, **kwargs):
        try:
            obj = get_object_or_404(Lesson, pk=request.data['lesson_id'])
            self.check_object_permissions(self.request, obj)
        except KeyError:
            pass
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=HTTP_201_CREATED)


class LessonStudentAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsStudent, OldLessonCompleted, IsOpenOrPurchased)
    serializer_class = LessonRetrieveSerializer
    queryset = Lesson.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        student = self.request.user
        change_student_lesson_view_statistics.delay(student_id=student.id, lesson_id=instance.id)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class LessonAPIView(LessonStudentAPIView):
    lookup_field = 'lesson_id'
    lookup_url_kwarg = 'pk'


class StudentLessonViewStatisticsAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = StudentLessonViewStatisticsSerializer

    def get_queryset(self):
        return StudentLessonViewStatistics.objects.filter(student=self.request.user).values(
            'viewed_date').annotate(count=Count('lesson')).order_by('-viewed_date')[:7]

    def get(self, request, *args, **kwargs):
        today_date = now().date()
        data1 = list(self.get_queryset())
        data2 = list(map(lambda el: el['viewed_date'], data1))
        response = []

        for i in range(7):
            obj = today_date

            if obj in data2:
                obj = data1[data2.index(obj)]
                response.append({'weekday': obj['viewed_date'].weekday(), 'count': obj['count']})
            else:
                response.append({'weekday': obj.weekday(), 'count': 0})
            today_date = today_date - timedelta(days=1)

        response.reverse()
        return Response(response)


class LessonQuestionAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsStudent, OldLessonCompletedForQuestions, IsOpenOrPurchased)
    serializer_class = QuestionSerializer
    queryset = Lesson.objects.all()

    def get(self, request, *args, **kwargs):
        questions = Question.objects.filter(lesson_id=self.kwargs[self.lookup_field])
        serializer = self.get_serializer(questions, many=True)
        return Response(serializer.data)

    def get_serializer_context(self):
        student_saved_question_list = StudentSavedQuestion.objects.filter(student=self.request.user).values(
            'question').order_by('question_id')
        question_text_list = QuestionDetail.objects.filter(language=get_language()).values('question', 'text').order_by(
            'question_id')
        category_name_list = CategoryDetail.objects.filter(language=get_language()).values('category', 'name').order_by(
            'category_id')
        variant_list = Variant.objects.filter(language=get_language(),
                                              question__lesson_id=self.kwargs[self.lookup_field]
                                              ).values('question', 'text', 'is_correct')
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'student_saved_question_list': student_saved_question_list,
            'question_text_list': question_text_list,
            'category_name_list': category_name_list,
            'variant_list': variant_list
        }

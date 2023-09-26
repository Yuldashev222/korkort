from datetime import timedelta

from django.db.models import Count
from django.utils.timezone import now
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.v1.lessons.tasks import change_student_lesson_view_statistics
from api.v1.lessons.models import LessonStudent, StudentLessonViewStatistics
from api.v1.exams.views.general import ExamAnswerAPIView
from api.v1.lessons.permissions import OldLessonCompleted, IsOpenOrPurchased, OldLessonCompletedForQuestions
from api.v1.lessons.serializers import (LessonRetrieveSerializer, StudentLessonViewStatisticsSerializer,
                                        LessonAnswerSerializer)
from api.v1.questions.models import StudentSavedQuestion, Question
from api.v1.accounts.permissions import IsStudent
from api.v1.questions.serializers.questions import QuestionSerializer


class LessonAnswerAPIView(ExamAnswerAPIView):
    serializer_class = LessonAnswerSerializer


class LessonStudentAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsStudent, OldLessonCompleted, IsOpenOrPurchased)
    serializer_class = LessonRetrieveSerializer

    def get_queryset(self):
        return LessonStudent.objects.filter(student=self.request.user).select_related('student')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        student = self.request.user
        change_student_lesson_view_statistics.delay(student_id=student.id, lesson_id=instance.lesson_id)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class LessonAPIView(LessonStudentAPIView):
    lookup_field = 'lesson_id'
    lookup_url_kwarg = 'pk'


class StudentLessonViewStatisticsAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = StudentLessonViewStatisticsSerializer

    def get_queryset(self):
        return StudentLessonViewStatistics.objects.filter(
            student=self.request.user).values('viewed_date').annotate(cnt=Count('lesson')).order_by('-viewed_date')[:7]

    def get(self, request, *args, **kwargs):
        today_date = now().date()
        response = []
        queryset = self.get_queryset()

        for i in range(7):
            try:
                obj = queryset[i]
            except IndexError:
                obj = {'viewed_date': today_date, 'cnt': 0}

            if obj['viewed_date'] != today_date:
                response.append({'count': 0, 'weekday': today_date.weekday()})
            else:
                response.append({'count': obj['cnt'], 'weekday': obj['viewed_date'].weekday()})

            today_date = today_date - timedelta(days=1)

        response.reverse()
        return Response(response)


class LessonQuestionAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsStudent, OldLessonCompletedForQuestions, IsOpenOrPurchased)
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return LessonStudent.objects.filter(student=self.request.user)

    def get(self, request, *args, **kwargs):
        questions = Question.objects.filter(lesson_id=self.get_object().lesson_id
                                            ).select_related('category').prefetch_related('variant_set')

        serializer = self.get_serializer(questions, many=True)
        return Response(serializer.data)

    def get_serializer_context(self):
        student_saved_question_ids = list(StudentSavedQuestion.objects.filter(
            student=self.request.user).values_list('question_id', flat=True).order_by('question_id'))
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'student_saved_question_ids': student_saved_question_ids
        }

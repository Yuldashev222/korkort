from django.db.models import Count
from rest_framework.generics import GenericAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.v1.exams.views.general import ExamAnswerAPIView
from api.v1.lessons.tasks import change_student_lesson_view_statistics
from api.v1.lessons.models import LessonStudent, StudentLessonViewStatistics
from api.v1.lessons.permissions import OldLessonCompleted, IsOpenOrPurchased
from api.v1.accounts.permissions import IsStudent
from api.v1.lessons.serializers import (LessonRetrieveSerializer, StudentLessonViewStatisticsSerializer,
                                        LessonAnswerSerializer)


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
        student = self.request.user
        return StudentLessonViewStatistics.objects.filter(student=student
                                                          ).values('viewed_date').annotate(cnt=Count('lesson'))[:7]

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

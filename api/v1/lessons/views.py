from django.db.models import Count
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from api.v1.exams.views import ExamAnswerAPIView
from api.v1.lessons.tasks import change_student_lesson_view_statistics
from api.v1.lessons.models import LessonStudent, StudentLessonViewStatistics
from api.v1.lessons.permissions import OldLessonCompleted, IsOpenOrPurchased
from api.v1.lessons.serializers import LessonRetrieveSerializer, StudentLessonViewStatisticsSerializer
from api.v1.accounts.permissions import IsStudent
from api.v1.questions.serializers.lessons import LessonAnswerSerializer


class LessonAnswerAPIView(ExamAnswerAPIView):
    serializer_class = LessonAnswerSerializer


class LessonAPIView(ReadOnlyModelViewSet):
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


class StudentLessonViewStatisticsAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = StudentLessonViewStatisticsSerializer

    def get_queryset(self):
        student = self.request.user
        queryset = StudentLessonViewStatistics.objects.filter(
            student=student).values('viewed_date').annotate(cnt=Count('viewed_date'))[:7]
        return queryset

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

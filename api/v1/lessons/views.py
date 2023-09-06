from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated

from api.v1.exams.views import ExamAnswerAPIView
from api.v1.lessons.tasks import change_student_lesson_view_statistics
from api.v1.lessons.models import LessonStudent, LessonStudentStatisticsByDay
from api.v1.lessons.permissions import OldLessonCompleted, IsOpenOrPurchased
from api.v1.lessons.serializers import LessonRetrieveSerializer, LessonStudentStatisticsByDaySerializer
from api.v1.accounts.permissions import IsStudent
from api.v1.questions.serializers.lessons import LessonAnswerSerializer


class LessonAnswerAPIView(ExamAnswerAPIView):
    serializer_class = LessonAnswerSerializer


class LessonAPIView(ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated, IsStudent, OldLessonCompleted, IsOpenOrPurchased)
    serializer_class = LessonRetrieveSerializer

    def get_queryset(self):
        return LessonStudent.objects.filter(student=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        student = self.request.user
        change_student_lesson_view_statistics.delay(student_id=student.id, lesson_id=instance.lesson_id)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class LessonStudentStatisticsByDayAPIView(ListModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = LessonStudentStatisticsByDaySerializer

    def get_queryset(self):
        student = self.request.user
        return LessonStudentStatisticsByDay.objects.filter(student=student)[:7]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

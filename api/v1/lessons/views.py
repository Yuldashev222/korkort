from datetime import timedelta

from django_filters import rest_framework as filters
from django.utils.timezone import now
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated

from api.v1.lessons.tasks import change_student_lesson_view_statistics
from api.v1.questions.models import LessonQuestion
from api.v1.lessons.permissions import OldLessonCompleted, IsOpenOrPurchased
from api.v1.accounts.permissions import IsStudent
from api.v1.questions.serializers import LessonQuestionSerializer

from api.v1.lessons.serializers import (
    LessonListSerializer,
    LessonWordInfoSerializer,
    LessonSourceSerializer,
    LessonRetrieveSerializer,
    LessonStudentStatisticsByDaySerializer
)

from api.v1.lessons.models import (
    LessonStudent,
    LessonWordInfo,
    LessonSource,
    LessonStudentStatisticsByDay
)


class LessonAPIView(ReadOnlyModelViewSet):
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('lesson__chapter',)
    permission_classes = (IsAuthenticated, IsStudent, OldLessonCompleted, IsOpenOrPurchased)

    def get_queryset(self):
        student = self.request.user
        return LessonStudent.objects.filter(student=student).select_related('lesson').order_by('lesson__ordering_number'
                                                                                               )

    def get_serializer_class(self):
        if self.action == 'list':
            return LessonListSerializer
        return LessonRetrieveSerializer

    def list(self, request, *args, **kwargs):
        if not (request.query_params.get('lesson__chapter') and request.query_params.get('language')):
            return Response([])
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        if not request.query_params.get('language'):
            return Response([])
        instance = self.get_object()
        student = self.request.user
        change_student_lesson_view_statistics.delay(student_id=student.id, lesson_id=instance.lesson_id)
        serializer = self.get_serializer(instance)
        data = {'main': serializer.data}

        word_info_queryset = LessonWordInfo.objects.filter(lessons__in=[instance.lesson])
        word_infos = LessonWordInfoSerializer(word_info_queryset, many=True, context={'request': request}).data
        data['word_infos'] = word_infos

        sources_queryset = LessonSource.objects.filter(lessons__in=[instance.lesson])
        sources = LessonSourceSerializer(sources_queryset, many=True, context={'request': request}).data
        data['sources'] = sources

        lessons_queryset = LessonStudent.objects.filter(lesson__chapter=instance.lesson.chapter, student=student
                                                        ).order_by('lesson__ordering_number')
        lessons = LessonListSerializer(lessons_queryset, many=True, context={'request': request}).data
        data['lessons'] = lessons

        questions_queryset = LessonQuestion.objects.filter(lesson=instance.lesson).order_by('ordering_number')
        questions = LessonQuestionSerializer(questions_queryset, many=True, context={'request': request}).data
        data['questions'] = questions

        return Response(data)


class LessonStudentStatisticsByDayAPIView(ListModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = LessonStudentStatisticsByDaySerializer

    def get_queryset(self):
        student = self.request.user
        today_date = now().date()
        return LessonStudentStatisticsByDay.objects.filter(student=student, date__gt=today_date - timedelta(days=7)
                                                           ).order_by('date')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

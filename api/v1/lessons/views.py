from django_filters import rest_framework as filters
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from api.v1.lessons.models import LessonStudent, LessonWordInfo, LessonSource
from api.v1.lessons.permissions import OldLessonCompleted, IsOpenOrPurchased
from api.v1.accounts.permissions import IsStudent
from api.v1.lessons.serializers import (
    LessonListSerializer,
    LessonWordInfoSerializer,
    LessonSourceSerializer,
    LessonRetrieveSerializer
)


class LessonAPIView(ReadOnlyModelViewSet):
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('lesson__chapter',)
    permission_classes = (IsAuthenticated, IsStudent, OldLessonCompleted, IsOpenOrPurchased)

    def get_queryset(self):
        student = self.request.user
        return LessonStudent.objects.filter(student=student).select_related('lesson'
                                                                            ).order_by('lesson__ordering_number')

    def get_serializer_class(self):
        if self.action == 'list':
            return LessonListSerializer
        return LessonRetrieveSerializer

    def list(self, request, *args, **kwargs):
        if not request.query_params.get('lesson__chapter'):
            return Response([])
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = {'main': serializer.data}

        word_info_queryset = LessonWordInfo.objects.filter(lessons__in=[instance.lesson])
        word_infos = LessonWordInfoSerializer(word_info_queryset, many=True).data
        data['word_infos'] = word_infos

        sources_queryset = LessonSource.objects.filter(lessons__in=[instance.lesson])
        sources = LessonSourceSerializer(sources_queryset, many=True).data
        data['sources'] = sources

        lessons_queryset = LessonStudent.objects.filter(lesson__chapter=instance.lesson.chapter)
        lessons = LessonListSerializer(lessons_queryset, many=True).data
        data['lessons'] = lessons

        return Response(data)

from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.v1.lessons.models import LessonStudent
from api.v1.lessons.permissions import OldLessonCompleted
from api.v1.lessons.serializers import LessonListSerializer
from api.v1.accounts.permissions import IsStudent


class LessonAPIView(ReadOnlyModelViewSet):
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('lesson__chapter',)
    permission_classes = (IsAuthenticated, IsStudent, OldLessonCompleted)

    def get_queryset(self):
        student = self.request.user
        return LessonStudent.objects.filter(student=student).order_by('lesson__ordering_number')

    def get_serializer_class(self):
        if self.action == 'list':
            return LessonListSerializer
        return LessonListSerializer  # last

    def list(self, request, *args, **kwargs):
        if not request.query_params.get('chapter'):
            return Response([])
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

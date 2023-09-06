from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from api.v1.chapters.models import ChapterStudent
from api.v1.accounts.permissions import IsStudent
from api.v1.chapters.serializers import ChapterSerializer


class ChapterAPIView(ListAPIView):
    serializer_class = ChapterSerializer
    permission_classes = (IsAuthenticated, IsStudent)

    def get_queryset(self):
        student = self.request.user
        return ChapterStudent.objects.filter(student=student).select_related('chapter')

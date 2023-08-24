from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from api.v1.chapters.models import Chapter
from api.v1.accounts.permissions import IsStudent
from api.v1.chapters.serializers import ChapterSerializer


class ChapterAPIView(ListAPIView):
    serializer_class = ChapterSerializer
    permission_classes = (IsAuthenticated, IsStudent)
    queryset = Chapter.objects.order_by('ordering_number')


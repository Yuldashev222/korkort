from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from api.v1.lessons.tasks import change_student_lesson_view_statistics
from api.v1.lessons.models import LessonStudent
from api.v1.chapters.models import ChapterStudent
from api.v1.lessons.serializers import LessonRetrieveSerializer
from api.v1.accounts.permissions import IsStudent
from api.v1.chapters.serializers import ChapterStudentSerializer


class ChapterStudentAPIView(ReadOnlyModelViewSet):
    serializer_class = ChapterStudentSerializer
    permission_classes = (IsAuthenticated, IsStudent)

    def get_queryset(self):
        student = self.request.user
        return ChapterStudent.objects.filter(student=student).select_related('chapter')

    def get_object(self):
        student = self.request.user
        chapter_student = get_object_or_404(ChapterStudent, pk=self.kwargs[self.lookup_field])

        obj = LessonStudent.objects.filter(lesson__chapter_id=chapter_student.chapter_id, student=student,
                                           is_completed=False).select_related('lesson').first()

        if obj:
            if obj.lesson.is_open:
                return obj

            elif student.tariff_expire_date <= now():
                return None

        else:
            obj = LessonStudent.objects.filter(lesson__chapter_id=chapter_student.chapter_id, student=student,
                                               is_completed=True).last()

        return obj

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            raise PermissionDenied()
        student = self.request.user
        change_student_lesson_view_statistics.delay(student_id=student.id, lesson_id=instance.lesson_id)
        serializer = LessonRetrieveSerializer(instance, context={'request': request})
        return Response(serializer.data)

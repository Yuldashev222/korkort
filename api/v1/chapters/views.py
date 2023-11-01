from django.utils.timezone import now
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.utils.translation import get_language
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from api.v1.lessons.tasks import change_student_lesson_view_statistics
from api.v1.lessons.models import LessonStudent, LessonDetail
from api.v1.chapters.models import Chapter, ChapterDetail, ChapterStudent
from api.v1.lessons.serializers import LessonRetrieveSerializer
from api.v1.accounts.permissions import IsStudent
from api.v1.chapters.serializers import ChapterSerializer


class ChapterAPIView(ReadOnlyModelViewSet):
    lesson_student = None
    serializer_class = ChapterSerializer
    permission_classes = (IsAuthenticated, IsStudent)
    queryset = Chapter.objects.order_by('ordering_number')

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()

        ctx['details'] = ChapterDetail.objects.filter(language_id=get_language()).values('chapter', 'title'
                                                                                         ).order_by('chapter')

        ctx['chapter_student_list'] = ChapterStudent.objects.filter(
            student_id=self.request.user.pk).values('chapter_id', 'completed_lessons').order_by('chapter_id')
        return ctx

    def get_object(self):
        student = self.request.user
        chapter = super().get_object()

        lesson_student = LessonStudent.objects.filter(lesson__chapter_id=chapter.pk, student_id=student.pk,
                                                      is_completed=False
                                                      ).select_related('lesson').first()
        if lesson_student:
            lesson = lesson_student.lesson

            if chapter.ordering_number != 1 and lesson.ordering_number == 1:
                return None

            if lesson.is_open:
                self.lesson_student = lesson_student
                return lesson

            if student.tariff_expire_date < now():
                lesson_student = LessonStudent.objects.filter(lesson__chapter_id=chapter.pk, student_id=student.pk,
                                                              lesson__is_open=True,
                                                              is_completed=True).select_related('lesson').last()

                if not lesson_student and chapter.ordering_number == 1:
                    lesson_student = LessonStudent.objects.filter(lesson__chapter_id=chapter.pk, student_id=student.pk,
                                                                  lesson__is_open=True).select_related('lesson').last()

        else:
            lesson_student = LessonStudent.objects.filter(lesson__chapter_id=chapter.pk, student_id=student.pk,
                                                          is_completed=True
                                                          ).select_related('lesson').last()

        if lesson_student:
            self.lesson_student = lesson_student
            return lesson_student.lesson
        return None

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            raise PermissionDenied()
        lesson_detail = get_object_or_404(LessonDetail, lesson_id=instance.pk, language_id=get_language())

        student = self.request.user
        change_student_lesson_view_statistics.delay(student_id=student.pk, lesson_id=instance.pk)
        serializer = LessonRetrieveSerializer(instance, context={'request': request})
        serializer.context['lesson_detail'] = lesson_detail
        return Response(serializer.data)

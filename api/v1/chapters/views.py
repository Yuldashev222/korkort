from django.utils.timezone import now
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.utils.translation import get_language
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from api.v1.lessons.tasks import change_student_lesson_view_statistics
from api.v1.lessons.models import LessonStudent, LessonDetail, Lesson
from api.v1.chapters.models import Chapter, ChapterDetail, ChapterStudent
from api.v1.lessons.serializers import LessonRetrieveSerializer
from api.v1.accounts.permissions import IsStudent
from api.v1.chapters.serializers import ChapterSerializer


class ChapterAPIView(ReadOnlyModelViewSet):
    serializer_class = ChapterSerializer
    permission_classes = (IsAuthenticated, IsStudent)

    def get_queryset(self):
        return Chapter.objects.filter(chapterdetail__language_id=get_language()).order_by('ordering_number')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()

        ctx['details'] = ChapterDetail.objects.filter(language_id=get_language()
                                                      ).values('chapter_id', 'title'
                                                               ).order_by('chapter__ordering_number')

        ctx['chapter_student_list'] = ChapterStudent.objects.filter(student_id=self.request.user.pk
                                                                    ).values('chapter_id', 'completed_lessons'
                                                                             ).order_by('chapter__ordering_number')
        return ctx

    def get_object(self):
        student = self.request.user
        chapter = super().get_object()

        lesson_student = LessonStudent.objects.filter(lesson__chapter_id=chapter.pk, student_id=student.pk,
                                                      is_completed=False
                                                      ).select_related('lesson'
                                                                       ).order_by('lesson__ordering_number').first()

        if not lesson_student:
            lesson_student = LessonStudent.objects.filter(lesson__chapter_id=chapter.pk, student_id=student.pk,
                                                          is_completed=True
                                                          ).select_related('lesson'
                                                                           ).order_by('lesson__ordering_number').last()

        if not lesson_student:
            raise PermissionDenied()

        if lesson_student.lesson.is_open:
            return lesson_student.lesson

        if not lesson_student.is_completed:

            if (
                    lesson_student.lesson.ordering_number == Lesson.objects.filter(chapter_id=chapter.pk
                                                                                   ).order_by('ordering_number'
                                                                                              ).first().ordering_number
                    and
                    LessonStudent.objects.filter(lesson__chapter__ordering_number__lt=chapter.ordering_number,
                                                 is_completed=False).exists()
            ):
                raise PermissionDenied()

        if student.tariff_expire_date < now():
            lesson_student = LessonStudent.objects.filter(lesson__chapter_id=chapter.pk, student_id=student.pk,
                                                          lesson__is_open=True, is_completed=True
                                                          ).select_related('lesson'
                                                                           ).order_by('lesson__ordering_number'
                                                                                      ).last()

            if not lesson_student:
                lesson_student = LessonStudent.objects.filter(lesson__chapter_id=chapter.pk, student_id=student.pk,
                                                              lesson__is_open=True
                                                              ).select_related('lesson'
                                                                               ).order_by('lesson__ordering_number'
                                                                                          ).last()
        if not lesson_student:
            raise PermissionDenied()

        return lesson_student.lesson

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        lesson_detail = get_object_or_404(LessonDetail, lesson_id=instance.pk, language_id=get_language())

        student = self.request.user
        serializer = LessonRetrieveSerializer(instance, context={'request': request})
        serializer.context['lesson_detail'] = lesson_detail
        change_student_lesson_view_statistics.delay(student_id=student.pk, lesson_id=instance.pk)
        return Response(serializer.data)

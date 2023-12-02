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
from api.v1.accounts.serializers import ProfileChapterSerializer
from api.v1.chapters.serializers import ChapterSerializer


class ChapterAPIView(ReadOnlyModelViewSet):
    serializer_class = ChapterSerializer
    permission_classes = (IsAuthenticated, IsStudent)

    def get_queryset(self):
        return Chapter.objects.filter(chapterdetail__language_id=get_language()).order_by('ordering_number')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = {
            'user': ProfileChapterSerializer(self.request.user).data,
            'chapters': serializer.data
        }
        return Response(data)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()

        if self.action == 'list':
            ctx['details'] = ChapterDetail.objects.filter(language_id=get_language()).values('chapter_id', 'title'
                                                                                             ).order_by('chapter_id')

            ctx['chapter_student_list'] = ChapterStudent.objects.filter(student_id=self.request.user.pk
                                                                        ).values('chapter_id', 'completed_lessons'
                                                                                 ).order_by('chapter_id')
        return ctx

    @property
    def get_object(self):
        student = self.request.user
        chapter = super().get_object()
        student_tariff_exists = student.tariff_expire_date > now().date()

        lesson_student_filter_kwargs = {'student_id': student.pk, 'lesson__chapter_id': chapter.pk}
        lesson_filter_kwargs = {'chapter_id': chapter.pk}
        if not student_tariff_exists:
            lesson_student_filter_kwargs['lesson__is_open'] = True
            lesson_filter_kwargs['is_open'] = True

        lesson_student = LessonStudent.objects.filter(**lesson_student_filter_kwargs, is_completed=False
                                                      ).order_by('lesson__ordering_number').last()

        if not lesson_student:
            lesson_student = LessonStudent.objects.filter(**lesson_student_filter_kwargs, is_completed=True
                                                          ).order_by('lesson__ordering_number').last()
        if not lesson_student:
            lesson = Lesson.objects.filter(**lesson_filter_kwargs).order_by('ordering_number').first()
        else:
            lesson = lesson_student.lesson  # last <select_related>

        if not lesson:
            raise PermissionDenied()

        return lesson

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object
        lesson_detail = get_object_or_404(LessonDetail, lesson_id=instance.pk, language_id=get_language())
        serializer = LessonRetrieveSerializer(instance, context={'request': request, 'lesson_detail': lesson_detail})
        change_student_lesson_view_statistics.delay(student_id=self.request.user.pk, lesson_id=instance.pk)
        return Response(serializer.data)

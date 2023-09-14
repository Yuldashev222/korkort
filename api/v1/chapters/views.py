from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from api.v1.lessons.tasks import change_student_lesson_view_statistics
from api.v1.lessons.models import LessonStudent
from api.v1.chapters.models import ChapterStudent
from api.v1.questions.models import StudentSavedQuestion
from api.v1.lessons.serializers import LessonRetrieveSerializer
from api.v1.accounts.permissions import IsStudent
from api.v1.chapters.serializers import ChapterStudentSerializer


class ChapterStudentAPIView(ReadOnlyModelViewSet):
    serializer_class = ChapterStudentSerializer
    permission_classes = (IsAuthenticated, IsStudent)

    def get_serializer_context(self):
        student_saved_question_ids = list(StudentSavedQuestion.objects.filter(
            student=self.request.user).values_list('question_id', flat=True).order_by('question_id'))
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'student_saved_question_ids': student_saved_question_ids
        }

    def get_queryset(self):
        student = self.request.user
        return ChapterStudent.objects.filter(student=student).select_related('chapter')

    def get_object(self):
        student = self.request.user
        try:
            chapter_student = ChapterStudent.objects.select_related('chapter').get(pk=self.kwargs[self.lookup_field])
            chapter = chapter_student.chapter
        except ChapterStudent.DoesNotExist:
            raise Http404({'detail': 'not found'})

        obj = LessonStudent.objects.filter(lesson__chapter_id=chapter.id, student=student, is_completed=False
                                           ).select_related('lesson').first()

        if obj:
            if chapter.ordering_number != 1 and obj.lesson.ordering_number == 1:
                return None

            if obj.lesson.is_open:
                return obj

            elif student.tariff_expire_date <= now():
                return None

        else:
            obj = LessonStudent.objects.filter(lesson__chapter_id=chapter.id, student=student, is_completed=True).last()

        return obj

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            raise PermissionDenied()
        student = self.request.user
        change_student_lesson_view_statistics.delay(student_id=student.id, lesson_id=instance.lesson_id)
        serializer = LessonRetrieveSerializer(instance, context=self.get_serializer_context())
        return Response(serializer.data)

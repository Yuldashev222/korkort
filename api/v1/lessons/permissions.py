from django.db.models import Sum
from django.utils.timezone import now
from rest_framework.permissions import BasePermission

from api.v1.chapters.models import ChapterStudent, Chapter
from api.v1.lessons.models import LessonStudent, Lesson


class OldLessonCompleted(BasePermission):
    def has_object_permission(self, request, view, obj):
        student, chapter = request.user, obj.chapter
        this_chapter_lessons = Lesson.objects.filter(chapter__ordering_number=chapter.ordering_number,
                                                     ordering_number__lt=obj.ordering_number).count()

        this_chapter_completed_lessons = LessonStudent.objects.filter(student_id=student.pk, is_completed=True,
                                                                      lesson__chapter__ordering_number=chapter.ordering_number,
                                                                      lesson__ordering_number__lt=obj.ordering_number
                                                                      ).count()
        if this_chapter_lessons != this_chapter_completed_lessons:
            return False

        old_chapters_lessons = Chapter.objects.filter(ordering_number__lt=chapter.ordering_number
                                                      ).aggregate(su=Sum('lessons', default=0))['su']

        old_chapters_completed_lessons = ChapterStudent.objects.filter(student_id=student.pk,
                                                                       chapter__ordering_number__lt=chapter.ordering_number
                                                                       ).aggregate(su=Sum('completed_lessons',
                                                                                          default=0))['su']
        return old_chapters_lessons == old_chapters_completed_lessons


class IsOpenOrPurchased(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.is_open or request.user.tariff_expire_date >= now().date()

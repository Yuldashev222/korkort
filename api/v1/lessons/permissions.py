from django.utils.timezone import now
from rest_framework.permissions import BasePermission

from api.v1.lessons.models import LessonStudent


class OldLessonCompleted(BasePermission):
    def has_object_permission(self, request, view, obj):
        student = request.user

        old_chapter_not_completed_lessons = LessonStudent.objects.filter(student_id=student.pk,
                                                                         is_completed=False,
                                                                         lesson__chapter__ordering_number__lt=obj.chapter.ordering_number,
                                                                         ).exists()

        this_chapter_not_completed_lessons = LessonStudent.objects.filter(student_id=student.pk,
                                                                          is_completed=False,
                                                                          lesson__chapter_id=obj.chapter_id,
                                                                          lesson__ordering_number__lt=obj.ordering_number,
                                                                          ).exists()

        return not (old_chapter_not_completed_lessons or this_chapter_not_completed_lessons)


class IsOpenOrPurchased(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.is_open or request.user.tariff_expire_date > now().date()

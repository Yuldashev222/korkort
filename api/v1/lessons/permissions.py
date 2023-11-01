from django.utils.timezone import now
from rest_framework.permissions import BasePermission

from api.v1.lessons.models import LessonStudent


class OldLessonCompleted(BasePermission):
    def has_object_permission(self, request, view, obj):
        student = request.user
        view.lesson_student = LessonStudent.objects.get(student_id=student.pk, lesson_id=obj.pk)
        if not view.lesson_student.is_completed and obj.ordering_number == 1:
            return False
        return not LessonStudent.objects.filter(lesson__chapter_id=obj.chapter.pk, student_id=student.pk,
                                                lesson__ordering_number__lt=obj.ordering_number,
                                                is_completed=False).exists()


class OldLessonCompletedForQuestions(BasePermission):
    def has_object_permission(self, request, view, obj):
        student = request.user
        return not LessonStudent.objects.filter(lesson__chapter_id=obj.chapter_id,
                                                student_id=student.pk,
                                                lesson__ordering_number__lt=obj.ordering_number,
                                                is_completed=False).exists()


class IsOpenOrPurchased(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.is_open or request.user.tariff_expire_date > now()

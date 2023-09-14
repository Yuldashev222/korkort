from django.utils.timezone import now
from rest_framework.permissions import BasePermission

from api.v1.lessons.models import LessonStudent


class OldLessonCompleted(BasePermission):
    def has_object_permission(self, request, view, obj):
        student = request.user
        if not obj.is_completed and obj.lesson.ordering_number == 1:
            return False

        return not LessonStudent.objects.filter(lesson__chapter=obj.lesson.chapter,
                                                student=student,
                                                lesson__ordering_number__lt=obj.lesson.ordering_number,
                                                is_completed=False).exists()


class IsOpenOrPurchased(BasePermission):
    def has_object_permission(self, request, view, obj):
        student = request.user
        if obj.lesson.is_open:
            return True
        return student.tariff_expire_date > now()

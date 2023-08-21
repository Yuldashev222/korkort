from rest_framework.permissions import BasePermission

from api.v1.lessons.models import LessonStudent


class OldLessonCompleted(BasePermission):
    def has_object_permission(self, request, view, obj):
        student = request.user
        return not LessonStudent.objects.filter(lesson__chapter=obj.lesson.chapter,
                                                lesson__ordering_number__lt=obj.lesson.ordering_number)

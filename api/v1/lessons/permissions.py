from rest_framework.permissions import BasePermission


class OldLessonCompleted(BasePermission):
    def has_object_permission(self, request, view, obj):
        student = request.user
        lesson = obj
        return

from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from api.v1.accounts.permissions import IsStudent
from api.v1.notifications.models import Notification
from api.v1.notifications.serializers import NotificationSerializer


class NotificationAPIView(ModelViewSet):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = NotificationSerializer

    def get_queryset(self):
        student = self.request.user
        queryset = Notification.objects.filter(
            Q(order__student_id=student.pk)
            |
            Q(swish_account__student_id=student.pk)
            |
            Q(student_id=student.pk)
            |
            Q(report__student_id=student.pk)
            |
            Q(tariff_discount__isnull=False)
        ).order_by('-viewed_at', '-created_at')

        return queryset

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['pk', 'notification_type', 'desc', 'is_viewed', 'created_at']
        read_only_fields = ['pk', 'notification_type', 'desc', 'created_at']

    def validate_is_viewed(self, value: bool) -> bool:
        if not value:
            raise ValidationError()
        return value

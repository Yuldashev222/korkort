from rest_framework import serializers

from api.v1.notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('notification_type', 'desc', 'is_viewed', 'created_at')

    def update(self, instance, validated_data):
        print(instance, validated_data)
        super().update(instance, validated_data)

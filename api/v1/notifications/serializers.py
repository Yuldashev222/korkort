from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.discounts.models import TariffDiscount
from api.v1.notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(read_only=True, allow_null=True)

    class Meta:
        model = Notification
        fields = ['pk', 'notification_type', 'desc', 'is_viewed', 'created_at', 'tariff_discount', 'image']
        read_only_fields = ['pk', 'notification_type', 'desc', 'created_at', 'image']

    def validate_is_viewed(self, value: bool) -> bool:
        if not value:
            raise ValidationError()
        return value

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if ret['notification_type'] == Notification.NOTIFICATION_TYPE[4][0]:
            ret['image'] = self.context['request'].build_absolute_uri(TariffDiscount.objects.last().image.url)
        return ret

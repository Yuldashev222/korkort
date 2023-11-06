from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied

from api.v1.swish.models import SwishCard, MinBonusMoney


class SwishCardSerializer(serializers.ModelSerializer):
    student = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SwishCard
        fields = ['number', 'student']

    def validate(self, attrs):
        min_bonus_money = MinBonusMoney.get_min_bonus_money()
        if not min_bonus_money:
            raise ValidationError('Does not work.')
        if self.context['request'].user.bonus_money < min_bonus_money:
            raise PermissionDenied()

        return attrs

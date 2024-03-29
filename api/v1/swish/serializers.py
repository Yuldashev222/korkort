from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied

from api.v1.swish.models import SwishCard, MinBonusMoney


class SwishCardSerializer(serializers.ModelSerializer):
    student = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SwishCard
        fields = ['number', 'student']

    def validate(self, attrs):
        obj = MinBonusMoney.objects.first()
        if not obj:
            raise ValidationError('Does not work.')
        if self.context['request'].user.bonus_money < obj.money:
            raise PermissionDenied()

        return attrs


class CalledStudentAndSwishTransactionSerializer(serializers.Serializer):
    is_income_copy = True
    is_income = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    student_name = serializers.SerializerMethodField()
    student_user_code = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return obj.created_at.date()

    def get_is_income(self, obj):
        self.is_income_copy = bool(obj.order)
        return self.is_income_copy

    def get_price(self, obj):
        return obj.order.user_code_discount_amount if self.is_income_copy else obj.swish_card.student_money

    def get_student_name(self, obj):
        return obj.order.student_name if self.is_income_copy else ''

    def get_student_user_code(self, obj):
        return obj.order.student_user_code if self.is_income_copy else ''

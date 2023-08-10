from django.core.cache import cache
from rest_framework import serializers

from .models import Tariff, TariffInfo


class TariffSerializer(serializers.ModelSerializer):
    student_discount_is_percent = serializers.BooleanField(default=False)
    student_discount_value = serializers.IntegerField(default=0)

    class Meta:
        model = Tariff
        exclude = ['tariff_info', 'discount', 'is_active', 'created_at']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if ret['student_discount']:
            student_discount = cache.get('student_discount')
            if student_discount:
                ret['student_discount_is_percent'] = student_discount['is_percent']
                if ret['student_discount_is_percent']:
                    ret['student_discount_value'] = student_discount['discount_value']
            else:
                ret['student_discount'] = False
                ret['student_discount_amount'] = 0
        return ret


class TariffInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TariffInfo
        fields = '__all__'

from rest_framework import serializers

from .models import TariffDay, Tariff


class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = TariffDay
        exclude = ['tariff', 'discount', 'student_discount_price', 'is_active', 'created_at']


class TariffInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = '__all__'

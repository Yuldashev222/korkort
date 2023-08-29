from rest_framework import serializers

from .models import Tariff, TariffInfo


class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        exclude = ['tariff_info', 'is_active', 'created_at']


class TariffInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TariffInfo
        fields = '__all__'

from rest_framework import serializers

from .models import Tariff


class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        exclude = ['is_active']

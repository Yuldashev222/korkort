from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.tariffs.models import Tariff


class StripeCheckoutSerializer(serializers.Serializer):
    tariff_id = serializers.IntegerField()

    def validate(self, attrs):
        tariff_id = attrs['tariff_id']
        try:
            tariff = Tariff.objects.get(pk=tariff_id)
        except Tariff.DoesNotExist:
            raise ValidationError({'tariff_id': 'not found'})

        attrs['tariff'] = tariff
        return attrs

from rest_framework import serializers

from api.v1.discounts.models import TariffDiscount


class TariffDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = TariffDiscount
        fields = ['title', 'image', 'is_percent', 'discount_value']

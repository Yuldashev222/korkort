from rest_framework import serializers

from api.v1.swish.models import SwishCard


class SwishCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = SwishCard
        fields = ['number']

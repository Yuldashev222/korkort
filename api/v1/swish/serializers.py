from rest_framework import serializers

from api.v1.swish.models import SwishCard


class SwishCardSerializer(serializers.ModelSerializer):
    student = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SwishCard
        fields = ['number', 'student']

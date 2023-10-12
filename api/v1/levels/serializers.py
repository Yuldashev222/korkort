from rest_framework import serializers

from api.v1.levels.models import Level


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'

from rest_framework import serializers

from api.v1.levels.models import Level
from api.v1.general.utils import bubble_search


class LevelSerializer(serializers.Serializer):
    ball = serializers.IntegerField(source='correct_answers')
    name = serializers.SerializerMethodField()

    def get_name(self, instance):
        sort_list = self.context['level_name_list']
        obj = bubble_search(instance.pk, 'level_id', sort_list)
        if obj is not None:
            return obj['name']
        return '-'

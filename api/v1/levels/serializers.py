from rest_framework import serializers

from api.v1.levels.models import Level
from api.v1.general.utils import bubble_search


class LevelSerializer(serializers.ModelSerializer):
    ball = serializers.IntegerField(source='correct_answers')

    class Meta:
        model = Level
        exclude = ['id', 'correct_answers']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['name'], ret['desc'] = self.get_level_name_and_desc(instance)
        return ret

    def get_level_name_and_desc(self, instance):
        sort_list = self.context['level_name_list']
        obj = bubble_search(instance.id, 'level', sort_list)
        if obj is not None:
            return obj['name'], obj['desc']
        return '-', '-'

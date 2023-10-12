from rest_framework import serializers

from api.v1.general.utils import bubble_search
from api.v1.levels.models import Level


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'

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

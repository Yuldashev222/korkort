from rest_framework import serializers

from .models import Tariff


class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        exclude = ['is_active', 'created_at']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        obj = list(filter(lambda el: el['tariff'] == instance.id, self.context['details']))[0]
        if obj:
            ret['title'] = obj['title']
            ret['desc'] = obj['desc']
        else:
            ret['title'] = ''
            ret['desc'] = ''
        return ret

from rest_framework import serializers

from api.v1.questions.models import Variant


class VariantSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()

    class Meta:
        model = Variant
        fields = ['id', 'is_correct', 'text']

    def get_text(self, instance):
        language = self.context['request'].query_params.get('language', '')
        return getattr(instance, 'text_' + language, None)

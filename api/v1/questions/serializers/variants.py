from rest_framework import serializers

from api.v1.general.utils import get_language
from api.v1.questions.models import Variant


class VariantSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()

    class Meta:
        model = Variant
        fields = ['id', 'is_correct', 'text']

    def get_text(self, instance):
        return getattr(instance, 'text_' + get_language(), None)

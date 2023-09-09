from rest_framework import serializers

from api.v1.general.utils import get_language
from api.v1.questions.serializers.variants import VariantSerializer


class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    question_text = serializers.SerializerMethodField()
    question_video = serializers.FileField(source='video')
    question_image = serializers.ImageField(source='image')

    variant_set = VariantSerializer(many=True)

    def get_question_text(self, instance):
        return getattr(instance, 'text_' + get_language())


class QuestionAnswerSerializer(serializers.Serializer):
    pk = serializers.IntegerField()

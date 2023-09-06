from rest_framework import serializers

from api.v1.questions.serializers.variants import VariantSerializer


class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    question_text = serializers.SerializerMethodField()
    question_video = serializers.SerializerMethodField()

    variant_set = VariantSerializer(many=True)

    def get_question_video(self, instance):
        request = self.context.get('request')
        language = request.query_params.get('language', '')
        if getattr(instance, 'video_' + language, None):
            return request.build_absolute_uri(eval(f'instance.video_{language}.url'))
        return None

    def get_question_text(self, instance):
        language = self.context['request'].query_params.get('language', '')
        return getattr(instance, 'text_' + language, None)


class QuestionAnswerSerializer(serializers.Serializer):
    pk = serializers.IntegerField()

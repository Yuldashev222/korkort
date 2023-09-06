from rest_framework import serializers

from api.v1.questions.models import StudentSavedQuestion


class SavedQuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSavedQuestion
        fields = ['question']


class SavedQuestionRetrieveSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()

    class Meta:
        model = StudentSavedQuestion
        fields = ['id', 'text', 'video', 'created_at']

    def get_text(self, instance):
        language = self.context['request'].query_params.get('language', '')
        return getattr(instance.question, 'text_' + language, None)

    def get_video(self, instance):
        request = self.context['request']
        language = request.query_params.get('language', '')

        if getattr(instance, 'video_' + language, None):
            return request.build_absolute_uri(eval(f'instance.video_{language}.url'))
        return None

from rest_framework import serializers

from api.v1.general.utils import get_language
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
        return getattr(instance.question, 'text_' + get_language())

    def get_video(self, instance):
        request = self.context['request']
        language = get_language()
        if getattr(instance, 'video_' + language, None):
            return request.build_absolute_uri(eval(f'instance.video_{language}.url'))
        return None

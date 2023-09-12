from rest_framework import serializers

from api.v1.general.utils import get_language
from api.v1.questions.models import StudentSavedQuestion
from api.v1.questions.serializers.variants import VariantSerializer


class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    question_text = serializers.SerializerMethodField()
    # question_video = serializers.FileField(source='video')
    question_video = serializers.URLField(default='http://16.171.170.49/media/questions/18000%3A%200fac9957-9516-4083-9ae4/videos/giphy.gif')
    # question_image = serializers.ImageField(source='image')
    question_image = serializers.URLField(default='http://16.171.170.49/media/chapters/1:%20836c4b38-fe8e-4ef2-9a9c-bab/lessons/1:%20905c9192-956f-4054-9ce1-161/images/Re_A8H4vJl.png')
    is_saved = serializers.SerializerMethodField()  # last

    variant_set = VariantSerializer(many=True)

    def get_is_saved(self, instance):
        try:
            StudentSavedQuestion.objects.get(question=instance)
        except StudentSavedQuestion.DoesNotExist:
            return False
        return True

    def get_question_text(self, instance):
        return getattr(instance, 'text_' + get_language())


class QuestionAnswerSerializer(serializers.Serializer):
    pk = serializers.IntegerField()

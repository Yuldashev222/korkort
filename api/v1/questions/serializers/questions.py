from rest_framework import serializers

from api.v1.general.utils import get_language
from api.v1.questions.models import StudentSavedQuestion, Question
from api.v1.questions.serializers.variants import VariantSerializer


class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    category_id = serializers.IntegerField()
    category = serializers.StringRelatedField()
    question_text = serializers.SerializerMethodField()
    # question_video = serializers.FileField(source='video')
    question_video = serializers.URLField(default='https://www.e-report.uz/media/chapters/1%3A%202014e1e9-a989-4995-b36f-77a/lessons/1%3A%207f319207-d48e-41c2-b6dd-ca2/videos/a.mp4')
    # question_image = serializers.ImageField(source='image')
    question_image = serializers.URLField(default='https://www.e-report.uz/media/chapters/1%3A%202014e1e9-a989-4995-b36f-77a/images/IMG.png')
    is_saved = serializers.SerializerMethodField()  # last

    variant_set = VariantSerializer(many=True)

    def get_is_saved(self, instance):
        if Question.is_correct_question_id(question_ids=self.context['student_saved_question_ids'],
                                           question_id=instance.id):
            return True
        return False

    def get_question_text(self, instance):
        return getattr(instance, 'text_' + get_language())


class QuestionAnswerSerializer(serializers.Serializer):
    pk = serializers.IntegerField()

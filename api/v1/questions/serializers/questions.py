from rest_framework import serializers

from api.v1.general.utils import get_language
from api.v1.questions.models import Question
from api.v1.questions.serializers.variants import VariantSerializer


class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    category_id = serializers.IntegerField()
    category = serializers.StringRelatedField()
    question_text = serializers.SerializerMethodField()
    # question_gif = serializers.FileField(source='gif')
    question_gif = serializers.URLField(default='http://51.20.2.33/media/questions/6000%3A_73f57c8b-13ed-447f-b39c-/gifs/giphy.gif')
    # gif_last_frame_number = serializers.IntegerField()
    gif_last_frame_number = serializers.IntegerField(default=24)
    # question_image = serializers.ImageField(source='image')
    question_image = serializers.URLField(default='http://51.20.2.33/media/chapters/1:_df478f64-8c95-4fe0-a9d2-30e/lessons/1:%208908c739-1de4-4f39-9d38-929/images/Re_z4gl9tD.png')
    is_saved = serializers.SerializerMethodField()

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

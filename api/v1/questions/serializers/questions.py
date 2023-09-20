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
    question_gif = serializers.URLField(default='http://91.226.221.227/media/questions/6000%3A_db7c0bab-b729-4081-8123-/gifs/giphy.gif')
    # gif_last_frame_number = serializers.IntegerField()
    question_gif_last_frame_number = serializers.IntegerField(default=24)
    # question_image = serializers.ImageField(source='image')
    question_image = serializers.URLField(default='http://91.226.221.227/media/chapters/1%3A_a04d16a9-155c-464d-82e5-e6d/images/Rectangle_625.png')
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

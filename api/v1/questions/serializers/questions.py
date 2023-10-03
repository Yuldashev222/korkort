import random

from rest_framework import serializers

from api.v1.general.utils import get_language
from api.v1.questions.models import Question
from api.v1.questions.serializers.variants import VariantSerializer
from api.v1.questions.tests import gifs


class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    category_id = serializers.IntegerField()
    category = serializers.SerializerMethodField()
    question_text = serializers.SerializerMethodField()
    # question_gif = serializers.FileField(source='gif')
    # question_gif_last_frame_number = serializers.IntegerField(default=1302)
    # question_gif_duration = serializers.IntegerField(default=59220)
    # question_image = serializers.ImageField(source='image')
    question_image = serializers.URLField(
        default='https://api.lattmedkorkort.se/media/chapters/1%3A_5663e70a-0c7b-4118-907a-be4/images/Rectangle_625.png')
    is_saved = serializers.SerializerMethodField()

    variant_set = VariantSerializer(many=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['question_gif'], ret['question_gif_last_frame_number'], ret['question_gif_duration'] = random.choice(gifs)
        return ret

    def get_is_saved(self, instance):
        return Question.is_correct_question_id(question_ids=self.context['student_saved_question_ids'],
                                               question_id=instance.id)

    def get_question_text(self, instance):
        return getattr(instance, 'text_' + get_language())

    def get_category(self, instance):
        return getattr(instance.category, 'name_' + get_language())


class QuestionAnswerSerializer(serializers.Serializer):
    pk = serializers.IntegerField()

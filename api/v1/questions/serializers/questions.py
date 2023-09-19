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
    question_gif = serializers.URLField(default='http://51.20.2.33/media/questions/6000%3A%2052a70a5f-6c1a-41af-b385-/gifs/giphy_PZKlRXf.gif')
    # question_image = serializers.ImageField(source='image')
    question_image = serializers.URLField(default='http://51.20.2.33/media/chapters/1:%20a940a76e-290f-46c7-ac6d-0a3/lessons/1:%2014303787-0823-44c8-a572-535/images/Re_hDa0ivt.png')
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

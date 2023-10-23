import random
from rest_framework import serializers

from api.v1.general.utils import bubble_search
from api.v1.questions.tests import gifs


class QuestionSerializer(serializers.Serializer):
    answer = None

    id = serializers.IntegerField()
    category_id = serializers.IntegerField()
    category = serializers.SerializerMethodField()
    # question_gif = serializers.FileField(source='gif')
    # question_gif_last_frame_number = serializers.IntegerField(default=1302)
    # question_gif_duration = serializers.IntegerField(default=59220)
    # question_image = serializers.ImageField(source='image')
    question_image = serializers.URLField(
        default='https://api.lattmedkorkort.se/media/chapters/1%3A_5663e70a-0c7b-4118-907a-be4/images/Rectangle_625.png')
    is_saved = serializers.SerializerMethodField()

    variants = serializers.SerializerMethodField()

    def get_variants(self, instance):
        variants = list(filter(lambda el: el['question'] == instance.id, self.context['variant_list']))
        random.shuffle(variants)
        return variants

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['question_gif'], ret['question_gif_last_frame_number'], ret['question_gif_duration'] = random.choice(gifs)
        ret['question_text'], self.answer = self.get_question_text_and_answer(instance)
        return ret

    def get_is_saved(self, instance):
        sort_list = self.context['student_saved_question_list']
        obj = bubble_search(instance.id, 'question', sort_list)
        if obj is not None:
            return True
        return False

    def get_question_text_and_answer(self, instance):
        sort_list = self.context['question_text_list']
        obj = bubble_search(instance.id, 'question', sort_list)
        if obj is not None:
            try:
                return obj['text'], obj['answer']
            except KeyError:
                return obj['text'], '-'
        return '-', '-'

    def get_category(self, instance):
        sort_list = self.context['category_name_list']
        obj = bubble_search(instance.category_id, 'category', sort_list)
        if obj is not None:
            return obj['name']
        return '-'


class QuestionAnswerSerializer(serializers.Serializer):
    pk = serializers.IntegerField()

import random
from rest_framework import serializers

from api.v1.general.utils import bubble_search
from api.v1.questions.tests import gifs


class QuestionSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    category_id = serializers.IntegerField()
    # question_gif = serializers.FileField(source='gif')
    # question_gif_last_frame_number = serializers.IntegerField(default=1302)
    # question_gif_duration = serializers.IntegerField(default=59220)
    # question_image = serializers.ImageField(source='image')
    image = serializers.URLField(
        default='https://api.lattmedkorkort.se/media/chapters/1%3A_5663e70a-0c7b-4118-907a-be4/images/Rectangle_625.png')
    is_saved = serializers.SerializerMethodField()

    variants = serializers.SerializerMethodField()

    def get_variants(self, instance):
        sort_list = self.context['question_text_list']
        obj = bubble_search(instance.pk, 'question_id', sort_list)
        variants = [
            {'text': obj['correct_variant'], 'is_correct': True}, {'text': obj['variant2'], 'is_correct': False}
        ]
        if obj['variant3']:
            variants.append({'text': obj['variant3'], 'is_correct': False})
        if obj['variant4']:
            variants.append({'text': obj['variant4'], 'is_correct': False})

        random.shuffle(variants)
        return variants

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['gif'], ret['gif_last_frame_number'], ret['gif_duration'] = random.choice(gifs)
        ret['text'], ret['answer'] = self.get_question_text_and_answer(instance)
        return ret

    def get_is_saved(self, instance):
        sort_list = self.context['student_saved_question_list']
        obj = bubble_search(instance.pk, 'question_id', sort_list)
        return bool(obj)

    def get_question_text_and_answer(self, instance):
        sort_list = self.context['question_text_list']
        obj = bubble_search(instance.pk, 'question_id', sort_list)
        return obj['text'], obj.get('answer', None)

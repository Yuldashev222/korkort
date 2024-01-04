import random
from rest_framework import serializers

from api.v1.general.utils import bubble_search


class QuestionSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    category_id = serializers.IntegerField()
    image = serializers.CharField(read_only=True)
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
        ret['video'] = 'https://api.lattmedkorkort.se/media/questions/videos/pexels-george-morina-5266783_1080p.mp4'
        ret['text'], ret['answer'] = self.get_question_text_and_answer(instance)
        ret['image'] = 'https://www.industrialempathy.com/img/remote/ZiClJf-1920w.jpg'
        return ret

    def get_is_saved(self, instance):
        sort_list = self.context['student_saved_question_list']
        obj = bubble_search(instance.pk, 'question_id', sort_list)
        return bool(obj)

    def get_question_text_and_answer(self, instance):
        sort_list = self.context['question_text_list']
        obj = bubble_search(instance.pk, 'question_id', sort_list)
        return obj['text'], obj.get('answer', None)

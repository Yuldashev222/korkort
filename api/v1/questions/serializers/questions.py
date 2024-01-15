import random
from rest_framework import serializers

from api.v1.general.utils import bubble_search
from api.v1.todos.tests import get_random_image


class QuestionSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    category_id = serializers.IntegerField()
    image = serializers.CharField(read_only=True)
    is_saved = serializers.SerializerMethodField()

    variants = serializers.SerializerMethodField()

    def get_variants(self, instance):
        sort_list = self.context['question_text_list']
        obj = bubble_search(instance.pk, 'question_id', sort_list)
        if not obj:
            return []

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
        ret['image'] = get_random_image()
        ret['text'], ret['answer'] = self.get_question_text_and_answer(instance)
        return ret

    def get_is_saved(self, instance):
        sort_list = self.context['student_saved_question_list']
        obj = bubble_search(instance.pk, 'question_id', sort_list)
        return bool(obj)

    def get_question_text_and_answer(self, instance):
        sort_list = self.context['question_text_list']
        obj = bubble_search(instance.pk, 'question_id', sort_list)
        if not obj:
            return '', None  # last
        return obj['text'], obj.get('answer', None)

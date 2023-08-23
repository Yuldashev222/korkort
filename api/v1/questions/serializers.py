from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.questions.models import Variant, ExamQuestion, LessonQuestion


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = ['is_correct', 'text_swe', 'text_en', 'text_easy_swe']


class LessonQuestionSerializer(serializers.Serializer):
    question_text_swe = serializers.CharField(source='text_swe')
    question_text_en = serializers.CharField(source='text_en')
    question_text_easy_swe = serializers.CharField(source='text_easy_swe')
    question_video_swe = serializers.SerializerMethodField(source='video_swe', method_name='get_video_swe')
    question_video_eng = serializers.SerializerMethodField(source='video_eng', method_name='get_video_eng')
    question_video_easy_swe = serializers.SerializerMethodField(source='video_easy_swe',
                                                                method_name='get_video_easy_swe')

    lessonvariant_set = VariantSerializer(many=True)

    def get_video_swe(self, instance):
        request = self.context.get('request')
        return request.build_absolute_uri(instance.video_swe.url)

    def get_video_eng(self, instance):
        request = self.context.get('request')
        return request.build_absolute_uri(instance.video_eng.url)

    def get_video_easy_swe(self, instance):
        request = self.context.get('request')
        return request.build_absolute_uri(instance.video_easy_swe.url)


class ExamAnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    variant_id = serializers.IntegerField()
    is_correct = serializers.BooleanField(default=False)

    def validate(self, attrs):
        question_id = attrs.get('question_id')
        variant_id = attrs.get('variant_id')
        try:
            question_model, variant_query = self.get_question_model_and_variant_query(variant_id, question_id)
            question = question_model.objects.get(id=question_id)
            variant = Variant.objects.get(**variant_query)
        except (ExamQuestion.DoesNotExist, Variant.DoesNotExist):
            raise ValidationError('question_id or variant_id not valid')

        if variant.is_correct:
            attrs['is_correct'] = True
        return attrs

    @staticmethod
    def get_question_model_and_variant_query(variant_id, question_id):
        return ExamQuestion, {'id': variant_id, 'exam_question': question_id}

    def save(self, **kwargs):
        answers = self.validated_data
        unique_question_ids = list()
        unique_answers = list()
        for answer in answers:  # last
            if answer['question_id'] not in unique_question_ids:
                unique_question_ids.append(answer['question_id'])
                unique_answers.append(answer)
        return answers


class LessonAnswerSerializer(ExamAnswerSerializer):

    @staticmethod
    def get_question_model_and_variant_query(variant_id, question_id):
        return LessonQuestion, {'id': variant_id, 'lesson_question': question_id}

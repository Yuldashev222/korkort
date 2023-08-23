from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.lessons.models import LessonStudent
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
        if instance.video_swe:
            return request.build_absolute_uri(instance.video_swe.url)
        return None

    def get_video_eng(self, instance):
        request = self.context.get('request')
        if instance.video_eng:
            return request.build_absolute_uri(instance.video_eng.url)
        return None

    def get_video_easy_swe(self, instance):
        request = self.context.get('request')
        if instance.video_easy_swe:
            return request.build_absolute_uri(instance.video_easy_swe.url)
        return None


class ExamAnswerListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        return 1


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


class QuestionAnswerSerializer(ExamAnswerSerializer):

    @staticmethod
    def get_question_model_and_variant_query(variant_id, question_id):
        return LessonQuestion, {'id': variant_id, 'lesson_question': question_id}


class LessonQuestionAnswerSerializer(serializers.Serializer):
    lesson_id = serializers.IntegerField()
    answers = QuestionAnswerSerializer(many=True)

    def validate_lesson_id(self, lesson_id):
        try:
            LessonStudent.objects.get(id=lesson_id, student=self.context['request'].user)
        except LessonStudent.DoesNotExist:
            raise ValidationError({'lesson_id': 'not found.'})
        return lesson_id

    @staticmethod
    def get_unique_answers(validated_data):
        unique_question_ids, unique_questions = [], []
        answers = validated_data['answers']
        for answer in answers:
            if answer['question_id'] not in unique_question_ids:
                unique_question_ids.append(answer['question_id'])
                unique_questions.append(answer)
        return unique_questions

    def save(self):
        lesson_id = self.validated_data['lesson_id']
        answers = self.get_unique_answers(self.validated_data)

        return 1

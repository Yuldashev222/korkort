from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.questions.models import LessonVariant, ExamQuestion, ExamVariant, LessonQuestion


class LessonVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonVariant
        fields = ['is_correct', 'text_swe', 'text_en', 'text_easy_swe']


class LessonQuestionSerializer(serializers.Serializer):
    question_text_swe = serializers.CharField(source='text_swe')
    question_text_en = serializers.CharField(source='text_en')
    question_text_easy_swe = serializers.CharField(source='text_easy_swe')
    question_video_swe = serializers.SerializerMethodField(source='video_swe', method_name='get_video_swe')
    question_video_eng = serializers.SerializerMethodField(source='video_eng', method_name='get_video_eng')
    question_video_easy_swe = serializers.SerializerMethodField(source='video_easy_swe',
                                                                method_name='get_video_easy_swe')

    lessonvariant_set = LessonVariantSerializer(many=True)

    def get_video_swe(self, instance):
        request = self.context.get('request')
        return request.build_absolute_uri(instance.video_swe.path)

    def get_video_eng(self, instance):
        request = self.context.get('request')
        return request.build_absolute_uri(instance.video_eng.path)

    def get_video_easy_swe(self, instance):
        request = self.context.get('request')
        return request.build_absolute_uri(instance.video_easy_swe.path)


class ExamAnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    variant_id = serializers.IntegerField()

    def validate(self, attrs):
        print(attrs)
        answer_type = self.context['request'].data.get('answer_type')
        question_id = attrs.get('question_id')
        variant_id = attrs.get('variant_id')
        try:
            if answer_type == 'exam':
                question = ExamQuestion.objects.get(id=question_id)
                variant = ExamVariant.objects.get(id=variant_id, question=question)
            else:
                question = LessonQuestion.objects.get(id=question_id)
                variant = LessonVariant.objects.get(id=variant_id, question=question)
        except (ExamQuestion.DoesNotExist, ExamVariant.DoesNotExist,
                LessonQuestion.DoesNotExist, LessonVariant.DoesNotExist):
            raise ValidationError('question_id or variant_id not valid')
        return attrs


class AnswerSerializer(serializers.Serializer):
    answer_type = serializers.ChoiceField(choices=[['lesson', 'lesson'], ['exam', 'exam']])
    answers = ExamAnswerSerializer(many=True)

    def validate(self, attrs):
        # print(attrs)
        return attrs

    def save(self, **kwargs):
        return {}

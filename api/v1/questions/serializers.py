from django.core.cache import cache
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.balls.models import TestBall
from api.v1.lessons.models import LessonStudent
from api.v1.questions.models import Variant, ExamQuestion, LessonQuestion


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = ['id', 'is_correct', 'text_swe', 'text_en', 'text_easy_swe']


class LessonQuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
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


class ExamAnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    variant_id = serializers.IntegerField()
    is_correct = serializers.BooleanField(default=False, read_only=True)

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
            try:
                attrs['lesson_id'] = question.lesson_id  # last | test
            except AttributeError:
                pass
        return attrs

    @staticmethod
    def get_question_model_and_variant_query(variant_id, question_id):
        return ExamQuestion, {'id': variant_id, 'exam_question': question_id}


class QuestionAnswerSerializer(ExamAnswerSerializer):

    @staticmethod
    def get_question_model_and_variant_query(variant_id, question_id):
        return LessonQuestion, {'id': variant_id, 'lesson_question': question_id}


class LessonQuestionAnswerSerializer(serializers.Serializer):
    lesson_student = None
    lesson_id = serializers.IntegerField()
    answers = QuestionAnswerSerializer(many=True, allow_null=True, required=False)

    def validate_lesson_id(self, lesson_id):
        try:
            lesson = LessonStudent.objects.get(id=lesson_id, student=self.context['request'].user)
        except LessonStudent.DoesNotExist:
            raise ValidationError({'lesson_id': 'not found.'})
        self.lesson_student = lesson
        return lesson_id

    @staticmethod
    def get_unique_answers(validated_data, lesson_id):
        unique_question_ids, unique_questions = [], []
        answers = validated_data['answers']
        for answer in answers:
            if (
                    answer.get('is_correct')
                    and
                    answer.get('lesson_id') == lesson_id
                    and
                    answer['question_id'] not in unique_question_ids
            ):
                unique_question_ids.append(answer['question_id'])
                unique_questions.append(answer)
        return unique_questions

    def save(self):
        answers = self.get_unique_answers(self.validated_data, self.lesson_student.lesson_id)
        if self.lesson_student is not None and answers:
            test_ball = cache.get('test_ball')
            if not test_ball:
                TestBall.set_redis()
                test_ball = cache.get('test_ball')
            if not test_ball:
                return

            self.lesson_student.ball = len(answers) * test_ball
            if len(answers) == self.lesson_student.lesson.lessonquestion_set.count():
                self.lesson_student.is_completed = True
            self.lesson_student.save()
        return {}

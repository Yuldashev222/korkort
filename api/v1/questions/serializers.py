from rest_framework import serializers
from django.core.cache import cache
from rest_framework.exceptions import ValidationError

from api.v1.balls.models import TestBall
from api.v1.lessons.models import LessonStudent
from api.v1.questions.models import Variant, ExamQuestion, LessonQuestion, WrongQuestionStudent, SavedQuestionStudent


class VariantSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()

    class Meta:
        model = Variant
        fields = ['id', 'is_correct', 'text']

    def get_text(self, instance):
        language = self.context['request'].query_params.get('language')
        return getattr(instance, 'text_' + language, None)


class LessonQuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    question_text = serializers.SerializerMethodField()
    question_video = serializers.SerializerMethodField()

    variant_set = VariantSerializer(many=True)

    def get_question_video(self, instance):
        request = self.context.get('request')
        language = self.context['request'].query_params.get('language')
        if getattr(instance, 'video_' + language, None):
            return request.build_absolute_uri(eval(f'instance.video_{language}.url'))
        return None

    def get_question_text(self, instance):
        language = self.context['request'].query_params.get('language')
        return getattr(instance, 'text_' + language, None)


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
        except (ExamQuestion.DoesNotExist, Variant.DoesNotExist, LessonQuestion.DoesNotExist):
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
        return unique_questions, unique_question_ids

    def save(self):
        student = self.context['request'].user
        answers, unique_question_ids = self.get_unique_answers(self.validated_data, self.lesson_student.lesson_id)
        if self.lesson_student is not None and answers:
            test_ball = cache.get('test_ball')
            if not test_ball:
                TestBall.set_redis()
                test_ball = cache.get('test_ball')
            if not test_ball:
                return

            self.lesson_student.ball = len(answers) * test_ball
            questions = self.lesson_student.lesson.lessonquestion_set.all()
            correct_answers_count = questions.count() - len(answers)
            if correct_answers_count == 0:
                self.lesson_student.is_completed = True
            else:
                for question in questions.exclude(id__in=[unique_question_ids]):
                    WrongQuestionStudent.objects.get_or_create(lesson_question=question, student=student)

            self.lesson_student.save()
        return {}


class SavedQuestionStudentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedQuestionStudent
        fields = ['exam_question', 'lesson_question']

    def validate(self, attrs):
        student = self.context['request'].user
        exam_question = attrs.get('exam_question')
        lesson_question = attrs.get('lesson_question')

        if exam_question and lesson_question or not (exam_question, lesson_question):
            raise ValidationError('choice exam or lesson')

        if exam_question and SavedQuestionStudent.objects.filter(exam_question=exam_question, student=student).exists():
            raise ValidationError({'exam_question': ['This field is already added.']})

        if lesson_question and SavedQuestionStudent.objects.filter(lesson_question=lesson_question,
                                                                   student=student).exists():
            raise ValidationError({'lesson_question': ['This field is already added.']})

        return attrs


class SavedQuestionStudentRetrieveSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()

    class Meta:
        model = SavedQuestionStudent
        fields = ['id', 'text', 'video', 'created_at']

    def get_text(self, instance):
        language = self.context['request'].query_params.get('language')
        if instance.exam_question:
            return getattr(instance.exam_question, 'text_' + language, None)
        return getattr(instance.lesson_question, 'text_' + language, None)

    def get_video(self, instance):
        request = self.context['request']
        language = request.query_params.get('language')
        if instance.exam_question:
            instance = instance.exam_question
        else:
            instance = instance.lesson_question

        if getattr(instance, 'video_' + language, None):
            return request.build_absolute_uri(eval(f'instance.video_{language}.url'))
        return None

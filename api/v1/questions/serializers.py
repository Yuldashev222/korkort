from rest_framework import serializers
from django.core.cache import cache
from rest_framework.exceptions import ValidationError

from api.v1.balls.models import TestBall
from api.v1.lessons.models import LessonStudent
from api.v1.questions.tasks import update_student_wrong_answers
from api.v1.questions.models import (
    Variant,
    Question,
    SavedQuestionStudent,
    QuestionStudentLastResult
)


class VariantSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()

    class Meta:
        model = Variant
        fields = ['id', 'is_correct', 'text']

    def get_text(self, instance):
        language = str(self.context['request'].query_params.get('language'))
        return getattr(instance, 'text_' + language, None)


class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    question_text = serializers.SerializerMethodField()
    question_video = serializers.SerializerMethodField()

    variant_set = VariantSerializer(many=True)

    def get_question_video(self, instance):
        request = self.context.get('request')
        language = str(request.query_params.get('language'))
        if getattr(instance, 'video_' + language, None):
            return request.build_absolute_uri(eval(f'instance.video_{language}.url'))
        return None

    def get_question_text(self, instance):
        language = str(self.context['request'].query_params.get('language'))
        return getattr(instance, 'text_' + language, None)


class AnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    variant_id = serializers.IntegerField()
    is_correct = serializers.BooleanField(default=False, read_only=True)

    def validate(self, attrs):
        question_id = attrs.get('question_id')
        variant_id = attrs.get('variant_id')
        try:
            question = Question.objects.get(id=question_id)
            variant = Variant.objects.get(id=variant_id, question=question)
        except (Question.DoesNotExist, Variant.DoesNotExist):
            raise ValidationError('question_id or variant_id not valid')

        if variant.is_correct:
            attrs['is_correct'] = True
            attrs['for_lesson'] = question.for_lesson
            attrs['lesson_id'] = question.lesson_id
        return attrs


class StudentAnswerSerializer(serializers.Serializer):
    lesson_student = None
    lesson_id = serializers.IntegerField()
    answers = AnswerSerializer(many=True, allow_null=True, required=False)

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
                    answer.get('is_correct') and answer['for_lesson']
                    and
                    answer['lesson_id'] == lesson_id
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
                return {}

            lesson = self.lesson_student.lesson
            questions = lesson.question_set.filter(for_lesson=True)
            questions_count = questions.count()
            wrong_answers_count = questions_count - len(answers)
            QuestionStudentLastResult.objects.create(correct_answers=len(answers), questions=questions_count,
                                                     student=student)
            if wrong_answers_count == 0:
                self.lesson_student.is_completed = True

            update_student_wrong_answers.delay(student.id, lesson.id, unique_question_ids, True)
            self.lesson_student.ball = len(answers) * test_ball
            self.lesson_student.save()
        return {}


class SavedQuestionStudentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedQuestionStudent
        fields = ['question', 'question']

    def validate(self, attrs):
        student = self.context['request'].user
        question = attrs.get('question')
        question = attrs.get('question')

        if question and question or not (question, question):
            raise ValidationError('choice exam or lesson')

        if question and SavedQuestionStudent.objects.filter(question=question, student=student).exists():
            raise ValidationError({'question': ['This field is already added.']})

        if question and SavedQuestionStudent.objects.filter(question=question,
                                                            student=student).exists():
            raise ValidationError({'question': ['This field is already added.']})

        return attrs


class SavedQuestionStudentRetrieveSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()

    class Meta:
        model = SavedQuestionStudent
        fields = ['id', 'text', 'video', 'created_at']

    def get_text(self, instance):
        language = self.context['request'].query_params.get('language')
        if instance.question:
            return getattr(instance.question, 'text_' + language, '')
        return getattr(instance.question, 'text_' + language, '')

    def get_video(self, instance):
        request = self.context['request']
        language = request.query_params.get('language')
        if instance.question:
            instance = instance.question
        else:
            instance = instance.question

        if getattr(instance, 'video_' + language, None):
            return request.build_absolute_uri(eval(f'instance.video_{language}.url'))
        return None

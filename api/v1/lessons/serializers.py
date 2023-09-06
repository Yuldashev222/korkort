from rest_framework import serializers

from api.v1.lessons.models import LessonWordInfo, LessonSource, LessonStudentStatisticsByDay, LessonStudent
from api.v1.questions.models import Question
from api.v1.questions.serializers.questions import QuestionSerializer


class LessonListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.SerializerMethodField()
    is_open = serializers.BooleanField(source='lesson.is_open')
    is_completed = serializers.BooleanField()
    lesson_time = serializers.IntegerField(source='lesson.lesson_time')

    def get_title(self, instance):
        language = self.context['request'].query_params.get('language')
        return getattr(instance.lesson, 'title_' + language, '')


class LessonWordInfoSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()
    info = serializers.SerializerMethodField()

    class Meta:
        model = LessonWordInfo
        fields = ['id', 'text', 'info']

    def get_text(self, instance):
        language = self.context['request'].query_params.get('language')
        return getattr(instance, 'text_' + language, '')

    def get_info(self, instance):
        language = self.context['request'].query_params.get('language')
        return getattr(instance, 'text_' + language, '')


class LessonSourceSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()

    class Meta:
        model = LessonSource
        fields = ['id', 'text', 'link']

    def get_text(self, instance):
        language = self.context['request'].query_params.get('language')
        return getattr(instance, 'text_' + language, '')


class LessonStudentStatisticsByDaySerializer(serializers.ModelSerializer):
    weekday = serializers.SerializerMethodField()

    def get_weekday(self, instance):
        return instance.date.weekday()

    class Meta:
        model = LessonStudentStatisticsByDay
        fields = ['count', 'weekday']


class LessonRetrieveSerializer(LessonListSerializer):
    image = serializers.FileField(source='lesson.image')
    text = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()
    word_infos = LessonWordInfoSerializer(source='lesson.lessonwordinfo_set', many=True)
    sources = LessonSourceSerializer(source='lesson.lessonsource_set', many=True)
    lessons = serializers.SerializerMethodField()
    questions = serializers.SerializerMethodField()

    def get_lessons(self, instance):
        queryset = LessonStudent.objects.filter(lesson__chapter=instance.lesson.chapter, student=instance.student
                                                ).order_by('lesson__ordering_number')
        return LessonListSerializer(queryset, many=True, context={'request': self.context['request']}).data

    def get_questions(self, instance):
        queryset = Question.objects.filter(lesson=instance.lesson, for_lesson=True).order_by('ordering_number')
        return QuestionSerializer(queryset, many=True, context={'request': self.context['request']}).data

    def get_text(self, instance):
        language = self.context['request'].query_params.get('language')
        return getattr(instance.lesson, 'text_' + language, '')

    def get_video(self, instance):
        request = self.context['request']
        language = request.query_params.get('language')

        if getattr(instance.lesson, 'video_' + language, None):
            return request.build_absolute_uri(eval(f'instance.lesson.video_{language}.url'))
        return None

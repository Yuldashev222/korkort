from rest_framework import serializers
from django.utils.timezone import now

from api.v1.general.utils import get_language
from api.v1.lessons.models import LessonWordInfo, LessonSource, LessonStudentStatisticsByDay, LessonStudent
from api.v1.questions.models import Question
from api.v1.questions.serializers.questions import QuestionSerializer


class LessonListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.SerializerMethodField()
    lesson_time = serializers.FloatField(source='lesson.lesson_time')
    lesson_permission = serializers.SerializerMethodField()
    pause = 1
    play = 2
    clock = 3
    buy_clock = 4

    def get_lesson_permission(self, instance):
        tariff_expire_date = instance.student.tariff_expire_date
        if not instance.lesson.is_open and tariff_expire_date <= now():
            return self.buy_clock

        if not instance.is_completed:
            return self.clock

        return self.play

    def get_title(self, instance):
        return getattr(instance.lesson, 'title_' + get_language())


class LessonWordInfoSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()
    info = serializers.SerializerMethodField()

    class Meta:
        model = LessonWordInfo
        fields = ['id', 'text', 'info']

    def get_text(self, instance):
        return getattr(instance, 'text_' + get_language())

    def get_info(self, instance):
        return getattr(instance, 'text_' + get_language())


class LessonSourceSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()

    class Meta:
        model = LessonSource
        fields = ['id', 'text', 'link']

    def get_text(self, instance):
        return getattr(instance, 'text_' + get_language())


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
        queryset = LessonStudent.objects.filter(lesson__chapter=instance.lesson.chapter, student=instance.student)
        lessons = LessonListSerializer(queryset, many=True, context={'request': self.context['request']}).data
        for idx, lesson in enumerate(lessons):
            if lesson['lesson_permission'] == LessonListSerializer.clock:
                lessons[idx]['lesson_permission'] = LessonListSerializer.play
                break
        return lessons

    def get_questions(self, instance):
        queryset = Question.objects.filter(lesson=instance.lesson, for_lesson=True)
        return QuestionSerializer(queryset, many=True, context={'request': self.context['request']}).data

    def get_text(self, instance):
        return getattr(instance.lesson, 'text_' + get_language())

    def get_video(self, instance):
        request = self.context['request']
        language = get_language()
        if getattr(instance.lesson, 'video_' + language, None):
            return request.build_absolute_uri(eval(f'instance.lesson.video_{language}.url'))
        return None

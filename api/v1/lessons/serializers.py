from rest_framework import serializers

from api.v1.lessons.models import LessonWordInfo, LessonSource, LessonStudentStatisticsByDay


class LessonListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.SerializerMethodField()
    is_open = serializers.BooleanField(source='lesson.is_open')
    is_completed = serializers.BooleanField()
    lesson_time = serializers.IntegerField(source='lesson.lesson_time')

    def get_title(self, instance):
        language = self.context['request'].query_params.get('language')
        return getattr(instance.lesson, 'title_' + language, '')


class LessonRetrieveSerializer(LessonListSerializer):
    image = serializers.FileField(source='lesson.image')
    text = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()

    def get_text(self, instance):
        language = self.context['request'].query_params.get('language')
        return getattr(instance.lesson, 'text_' + language, '')

    def get_video(self, instance):
        request = self.context['request']
        language = request.query_params.get('language')

        if getattr(instance.lesson, 'video_' + language, None):
            return request.build_absolute_uri(eval(f'instance.lesson.video_{language}.url'))
        return None


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

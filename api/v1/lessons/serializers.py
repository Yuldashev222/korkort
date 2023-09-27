from django.conf import settings
from rest_framework import serializers
from django.utils.timezone import now
from rest_framework.exceptions import ValidationError

from api.v1.exams.models import StudentLastExamResult
from api.v1.general.utils import get_language
from api.v1.lessons.models import LessonWordInfo, LessonSource, LessonStudent
from api.v1.questions.tasks import update_student_wrong_answers, update_student_correct_answers
from api.v1.questions.models import Question
from api.v1.questions.serializers.questions import QuestionSerializer, QuestionAnswerSerializer


class LessonListSerializer(serializers.Serializer):
    old_obj = None
    pause = 1
    play = 2
    clock = 3
    buy_clock = 4
    id = serializers.IntegerField()
    title = serializers.SerializerMethodField()
    lesson_time = serializers.FloatField(source='lesson.lesson_time')
    lesson_permission = serializers.SerializerMethodField()

    def get_lesson_permission(self, instance):
        temp = self.clock
        tariff_expire_date = self.context['request'].user.tariff_expire_date
        if not instance.lesson.is_open and tariff_expire_date <= now():
            temp = self.buy_clock

        elif not self.old_obj:
            temp = self.play

        elif self.old_obj.is_completed:
            temp = self.play

        self.old_obj = instance
        return temp

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
        return getattr(instance, 'info_' + get_language())


class LessonSourceSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()

    class Meta:
        model = LessonSource
        fields = ['id', 'text', 'link']

    def get_text(self, instance):
        return getattr(instance, 'text_' + get_language())


class StudentLessonViewStatisticsSerializer(serializers.Serializer):
    weekday = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

    def get_count(self, instance):
        return instance['cnt']

    def get_weekday(self, instance):
        return instance['viewed_date'].weekday()


class LessonRetrieveSerializer(LessonListSerializer):
    # image = serializers.FileField(source='lesson.image')
    image = serializers.URLField(
        default='https://api.lattmedkorkort.se/media/chapters/1%3A_5663e70a-0c7b-4118-907a-be4/images/Rectangle_625.png')
    text = serializers.SerializerMethodField()
    # video = serializers.SerializerMethodField()
    video = serializers.URLField(
        default='https://offentligabeslut.se/wp-content/uploads/2023/06/Kopia-av-Namnlos-design-1.mp4')
    word_infos = LessonWordInfoSerializer(source='lesson.lessonwordinfo_set', many=True)
    sources = LessonSourceSerializer(source='lesson.lessonsource_set', many=True)
    lessons = serializers.SerializerMethodField()

    def get_lessons(self, instance):
        student = self.context['request'].user
        queryset = LessonStudent.objects.filter(lesson__chapter=instance.lesson.chapter, student=student
                                                ).select_related('lesson')
        lessons = LessonListSerializer(queryset, many=True, context=self.context).data
        return lessons

    def get_text(self, instance):
        return getattr(instance.lesson, 'text_' + get_language())

    def get_video(self, instance):
        request = self.context['request']
        language = get_language()
        if getattr(instance.lesson, 'video_' + language, None):
            return request.build_absolute_uri(eval(f'instance.lesson.video_{language}.url'))
        return None


class LessonAnswerSerializer(serializers.Serializer):
    lesson_id = serializers.IntegerField()
    questions = serializers.ListSerializer(child=QuestionAnswerSerializer(), max_length=settings.MAX_QUESTIONS)

    def to_internal_value(self, data):
        super().to_internal_value(data)
        lesson_id = data['lesson_id']
        student = self.context['request'].user

        try:
            lesson_student = LessonStudent.objects.select_related('lesson').get(id=lesson_id, student=student)
            lesson = lesson_student.lesson
        except LessonStudent.DoesNotExist:
            raise ValidationError({'lesson_id': 'not found.'})

        question_ids = list(set(question['pk'] for question in data['questions']))

        for pk in question_ids:
            if not Question.is_correct_question_id(question_id=pk):
                raise ValidationError({'pk': 'not found'})

        wrong_answers_cnt = len(question_ids)
        correct_question_ids = list(lesson.question_set.exclude(id__in=question_ids).values_list('pk', flat=True))  # last
        lesson_all_questions_cnt = wrong_answers_cnt + len(correct_question_ids)
        StudentLastExamResult.objects.create(wrong_answers=wrong_answers_cnt, questions=lesson_all_questions_cnt,
                                             student=student)
        if wrong_answers_cnt == 0:
            lesson_student.is_completed = True

        lesson_student.ball = (lesson_all_questions_cnt - wrong_answers_cnt) * settings.TEST_BALL
        lesson_student.save()

        update_student_correct_answers(student=student, correct_question_ids=correct_question_ids,
                                       wrong_question_ids=question_ids)
        update_student_wrong_answers.delay(correct_question_ids=correct_question_ids, wrong_question_ids=question_ids,
                                           lesson_id=lesson.id, student_id=student.id)

        return data

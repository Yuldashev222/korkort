from django.conf import settings
from rest_framework import serializers
from django.utils.timezone import now
from django.utils.translation import get_language
from rest_framework.exceptions import ValidationError

from api.v1.exams.models import StudentLastExamResult
from api.v1.general.utils import bubble_search
from api.v1.lessons.models import LessonWordInfo, LessonSource, LessonStudent, LessonDetail
from api.v1.questions.tasks import update_student_wrong_answers, update_student_correct_answers
from api.v1.questions.models import Question
from api.v1.questions.serializers.questions import QuestionAnswerSerializer


class LessonListSerializer(serializers.Serializer):
    old_obj = None
    pause = 1
    play = 2
    clock = 3
    buy_clock = 4

    id = serializers.IntegerField(source='lesson_id')
    lesson_time = serializers.FloatField(source='lesson.lesson_time')
    title = serializers.SerializerMethodField()
    lesson_permission = serializers.SerializerMethodField()

    def get_title(self, instance):
        sort_list = self.context['lesson_title_list']
        obj = bubble_search(instance.lesson.id, 'lesson', sort_list)
        if obj is not None:
            return obj['title']
        return '-'

    def get_lesson_permission(self, instance):
        temp = self.clock
        tariff_expire_date = self.context['student'].tariff_expire_date
        if not instance.lesson.is_open and tariff_expire_date <= now():
            temp = self.buy_clock

        elif not self.old_obj:
            temp = self.play

        elif self.old_obj.is_completed:
            temp = self.play

        self.old_obj = instance
        return temp


class LessonWordInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonWordInfo
        fields = ['id', 'word', 'info']


class LessonSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonSource
        fields = ['id', 'text', 'link']


class StudentLessonViewStatisticsSerializer(serializers.Serializer):
    weekday = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

    def get_count(self, instance):
        return instance['cnt']

    def get_weekday(self, instance):
        return instance['viewed_date'].weekday()


class LessonRetrieveSerializer(serializers.Serializer):
    video = 'https://api.lattmedkorkort.se/media/chapters/1%3A_26d7f4b6-6923-4612-9719-73a/lessons/1%3A%20193fe385-404e-4dff-a59b-7e5/videos/y2mate.is_-_Varning_f%C3%B6r_v%C3%A4gkorsning_10_k%C3%B6rkortsfr%C3%A5gor-2Je8t-zIWDc-1080pp-1696332751.mp4'
    id = serializers.IntegerField()
    lesson_time = serializers.FloatField()

    # image = serializers.FileField(source='lesson.image')
    image = 'https://api.lattmedkorkort.se/media/chapters/1%3A_5663e70a-0c7b-4118-907a-be4/images/Rectangle_625.png'

    lessons = serializers.SerializerMethodField()
    word_infos = serializers.SerializerMethodField()
    sources = serializers.SerializerMethodField()

    def get_lessons(self, instance):
        student = self.context['request'].user
        queryset = list(LessonStudent.objects.filter(lesson__chapter_id=instance.chapter_id, student=student
                                                     ).select_related('lesson'))
        ctx = {
            'student': self.context['request'].user,
            'lesson_title_list': LessonDetail.objects.filter(language=get_language(), lesson__lessonstudent__in=queryset
                                                             ).values('lesson', 'title').order_by('lesson')
        }
        lessons = LessonListSerializer(queryset, many=True, context=ctx).data
        return lessons

    def get_word_infos(self, instance):
        return LessonWordInfoSerializer(LessonWordInfo.objects.filter(lesson=instance, language=get_language()),
                                        many=True).data

    def get_sources(self, instance):
        return LessonSourceSerializer(LessonSource.objects.filter(lesson=instance, language=get_language()),
                                      many=True).data

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['image'] = self.image
        obj = LessonDetail.objects.get(lesson=instance, language=get_language())
        if obj:
            ret['text'] = obj.text
            ret['title'] = obj.title
            # if obj.video:
            #     ret['video'] = self.context['request'].build_absolute_uri(obj.video)
            # else:  # last
            ret['video'] = self.video

        else:
            ret['text'] = ''
            ret['title'] = ''
            ret['video'] = None
        return ret


class LessonAnswerSerializer(serializers.Serializer):
    lesson_id = serializers.IntegerField()
    questions = serializers.ListSerializer(child=QuestionAnswerSerializer(), max_length=settings.MAX_QUESTIONS)

    def to_internal_value(self, data):
        super().to_internal_value(data)
        lesson_id = data['lesson_id']
        student = self.context['request'].user

        try:
            lesson_student = LessonStudent.objects.select_related('lesson').get(lesson_id=lesson_id, student=student)
            lesson = lesson_student.lesson
        except LessonStudent.DoesNotExist:
            raise ValidationError({'lesson_id': 'not found.'})

        question_ids = list(set(question['pk'] for question in data['questions']))

        for pk in question_ids:
            if not Question.is_correct_question_id(question_id=pk):
                raise ValidationError({'pk': 'not found'})

        wrong_answers_cnt = len(question_ids)
        correct_question_ids = list(
            lesson.question_set.exclude(id__in=question_ids).values_list('pk', flat=True))  # last
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

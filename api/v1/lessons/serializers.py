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


class LessonListSerializer(serializers.Serializer):
    old_obj = None
    play = 2
    clock = 3
    buy_clock = 4

    id = serializers.IntegerField(source='lesson_id')
    lesson_time = serializers.FloatField(source='lesson.lesson_time')
    title = serializers.SerializerMethodField()
    is_open = serializers.SerializerMethodField()

    def get_title(self, instance):
        sort_list = self.context['lesson_title_list']
        obj = bubble_search(instance.lesson.pk, 'lesson_id', sort_list)
        return obj['title']

    def get_is_open(self, instance):
        temp = self.clock
        tariff_expire_date = self.context['student'].tariff_expire_date

        if self.old_obj is None:
            temp = self.play

        elif not instance.lesson.is_open and tariff_expire_date <= now().date():
            temp = self.buy_clock

        elif self.old_obj.is_completed:
            temp = self.play

        self.old_obj = instance
        return temp


class LessonWordInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonWordInfo
        fields = ['word', 'info']


class LessonSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonSource
        fields = ['text', 'link']


class StudentLessonViewStatisticsSerializer(serializers.Serializer):
    weekday = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

    def get_count(self, instance):
        return instance['cnt']

    def get_weekday(self, instance):
        return instance['viewed_date'].weekday()


class LessonRetrieveSerializer(serializers.Serializer):
    video = 'https://api.lattmedkorkort.se/media/lessons/videos/y2mate.is_-_Varning_f%C3%B6r_v%C3%A4gkorsning_10_k%C3%B6rkortsfr%C3%A5gor-2Je8t-zIWDc-1080pp-1696332751.mp4'
    image = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRClGlxrlqY7RlZZ_8PqNU0NfQOlqHUvPg9S80O8H1luMigslACzs8Aqggw1irL3tMIg1Y&usqp=CAU'
    id = serializers.IntegerField()
    title = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()
    lesson_time = serializers.FloatField()
    lessons = serializers.SerializerMethodField()
    word_infos = serializers.SerializerMethodField()
    sources = serializers.SerializerMethodField()

    def get_text(self, instance):
        return self.context['lesson_detail'].text

    def get_title(self, instance):
        return self.context['lesson_detail'].title

    def get_lessons(self, instance):
        student = self.context['request'].user
        queryset = LessonStudent.objects.filter(lesson__chapter_id=instance.chapter_id, student_id=student.pk
                                                ).select_related('lesson').order_by('lesson__ordering_number')
        ctx = {
            'student': self.context['request'].user,
            'lesson_title_list': LessonDetail.objects.filter(language_id=get_language(),
                                                             lesson__chapter_id=instance.chapter_id
                                                             ).values('lesson_id', 'title').order_by('lesson_id')
        }
        return LessonListSerializer(queryset, many=True, context=ctx).data

    def get_word_infos(self, instance):
        lesson_detail = self.context['lesson_detail']
        word_infos = LessonWordInfo.objects.filter(lesson_detail_id=lesson_detail.pk)
        return LessonWordInfoSerializer(word_infos, many=True).data

    def get_sources(self, instance):
        lesson_detail = self.context['lesson_detail']
        sources = LessonSource.objects.filter(lesson_detail_id=lesson_detail.pk)
        return LessonSourceSerializer(sources, many=True).data

    def to_representation(self, instance):  # last
        ret = super().to_representation(instance)
        ret['image'] = self.image
        ret['video'] = self.video
        return ret


class LessonAnswerSerializer(serializers.Serializer):
    lesson_id = serializers.IntegerField()
    wrong_question_id_list = serializers.ListField(child=serializers.IntegerField(), max_length=settings.MAX_QUESTIONS)
    correct_question_id_list = serializers.ListField(child=serializers.IntegerField(),
                                                     max_length=settings.MAX_QUESTIONS)

    def to_internal_value(self, data):
        super().to_internal_value(data)
        student = self.context['request'].user
        lesson_id = data['lesson_id']
        wrong_question_id_list = list(set(data['wrong_question_id_list']))
        correct_question_id_list = list(set(data['correct_question_id_list']))
        correct_question_id_list = [i for i in correct_question_id_list if i not in wrong_question_id_list]

        try:
            lesson_student = LessonStudent.objects.select_related('lesson').get(lesson_id=lesson_id,
                                                                                student_id=student.pk)
            lesson = lesson_student.lesson
        except LessonStudent.DoesNotExist:
            raise ValidationError({'lesson_id': 'not found.'})

        all_student_answer_question_id_list = wrong_question_id_list + correct_question_id_list
        all_lesson_question_id_list = list(Question.objects.filter(lesson_id=lesson.pk).values_list('pk', flat=True))
        if sorted(all_lesson_question_id_list) != sorted(all_student_answer_question_id_list):
            raise ValidationError({'detail': 'questions for lesson does not exist.'})

        for question_ids in [correct_question_id_list, wrong_question_id_list]:  # last
            for pk in question_ids:
                if not Question.is_correct_question_id(question_id=pk):
                    raise ValidationError({'question_id': 'not found'})

        wrong_question_count = len(wrong_question_id_list)
        correct_question_count = len(correct_question_id_list)

        StudentLastExamResult.objects.create(wrong_answers=wrong_question_count, student_id=student.pk,
                                             questions=wrong_question_count + correct_question_count)

        if wrong_question_count == 0:
            lesson_student.is_completed = True

        lesson_student.ball = correct_question_count * settings.TEST_BALL
        lesson_student.save()

        update_student_correct_answers(student=student, wrong_question_ids=wrong_question_id_list,
                                       correct_question_ids=correct_question_id_list)
        update_student_wrong_answers.delay(student_id=student.pk, wrong_question_ids=wrong_question_id_list,
                                           correct_question_ids=correct_question_id_list)

        return data

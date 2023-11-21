import random
from datetime import timedelta
from django.db.models import Count
from django.core.cache import cache
from django.utils.timezone import now
from rest_framework.status import HTTP_201_CREATED
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, RetrieveAPIView, get_object_or_404
from django.utils.translation import get_language
from rest_framework.permissions import IsAuthenticated

from api.v1.accounts.services import get_student_level
from api.v1.general.utils import bubble_search
from api.v1.lessons.tasks import change_student_lesson_view_statistics
from api.v1.lessons.models import StudentLessonViewStatistics, Lesson, LessonStudent, LessonDetail
from api.v1.levels.models import LevelDetail
from api.v1.questions.models import StudentSavedQuestion, Question, QuestionDetail
from api.v1.lessons.permissions import OldLessonCompleted, IsOpenOrPurchased
from api.v1.lessons.serializers import (LessonRetrieveSerializer, StudentLessonViewStatisticsSerializer,
                                        LessonAnswerSerializer, LessonListSerializer)
from api.v1.accounts.permissions import IsStudent
from api.v1.questions.serializers.questions import QuestionSerializer


class LessonAnswerAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsStudent, IsOpenOrPurchased, OldLessonCompleted)
    serializer_class = LessonAnswerSerializer

    def post(self, request, *args, **kwargs):
        student = self.request.user
        old_level_id = student.level_id
        try:
            obj = Lesson.objects.get(pk=request.data.get('lesson_id'))
            self.check_object_permissions(self.request, obj)
        except (Lesson.DoesNotExist, ValueError):
            pass

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(get_student_level(student, old_level_id), status=HTTP_201_CREATED)


class LessonStudentAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsStudent, IsOpenOrPurchased, OldLessonCompleted)
    serializer_class = LessonRetrieveSerializer

    def get_queryset(self):
        return Lesson.objects.filter(lessondetail__language_id=get_language())

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        student = self.request.user
        page = str(request.build_absolute_uri())
        change_student_lesson_view_statistics.delay(student_id=student.pk, lesson_id=instance.pk)

        page_cache = cache.get(page)
        if page_cache:
            queryset = LessonStudent.objects.filter(lesson__chapter_id=instance.chapter_id, student_id=student.pk
                                                    ).select_related('lesson')
            ctx = {
                'student': student,
                'lesson_title_list': LessonDetail.objects.filter(language_id=get_language(),
                                                                 lesson__lessonstudent__in=queryset
                                                                 ).values('lesson_id', 'title').order_by('lesson_id')
            }

            page_cache['lessons'] = LessonListSerializer(queryset, many=True, context=ctx).data
            return Response(page_cache)

        serializer = self.get_serializer(instance)
        serializer.context['lesson_detail'] = get_object_or_404(LessonDetail, lesson_id=instance.pk,
                                                                language_id=get_language())
        cache.set(page, serializer.data)
        return Response(serializer.data)


class StudentLessonViewStatisticsAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = StudentLessonViewStatisticsSerializer

    def get_queryset(self):
        return StudentLessonViewStatistics.objects.filter(student_id=self.request.user.pk).values(
            'viewed_date').annotate(count=Count('lesson')).order_by('-viewed_date')[:7]

    def get(self, request, *args, **kwargs):
        today_date = now().date()
        data1 = list(self.get_queryset())
        data2 = list(map(lambda el: el['viewed_date'], data1))
        response = []

        for i in range(7):
            obj = today_date

            if obj in data2:
                obj = data1[data2.index(obj)]
                response.append({'weekday': obj['viewed_date'].weekday(), 'count': obj['count']})
            else:
                response.append({'weekday': obj.weekday(), 'count': 0})
            today_date = today_date - timedelta(days=1)

        response.reverse()
        return Response(response)


class LessonQuestionAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsStudent, IsOpenOrPurchased, OldLessonCompleted)
    serializer_class = QuestionSerializer
    queryset = Lesson.objects.all()

    def get(self, request, *args, **kwargs):
        self.get_object()

        page = str(request.build_absolute_uri())
        page_cache = cache.get(page)
        if page_cache:
            sort_list = StudentSavedQuestion.objects.filter(student_id=self.request.user.pk
                                                            ).values('question_id').order_by('question_id')
            for i in page_cache:
                obj = bubble_search(i['pk'], 'question_id', sort_list)
                i['is_saved'] = bool(obj)
                random.shuffle(i['variants'])
            return Response(page_cache)

        questions = Question.objects.filter(lesson_id=self.kwargs[self.lookup_field],
                                            questiondetail__language_id=get_language()).order_by('ordering_number')

        serializer = self.get_serializer(questions, many=True)
        cache.set(page, serializer.data)
        return Response(serializer.data)

    def get_serializer_context(self):
        student_saved_question_list = StudentSavedQuestion.objects.filter(student_id=self.request.user.pk
                                                                          ).values('question_id'
                                                                                   ).order_by('question_id')

        question_text_list = QuestionDetail.objects.filter(language_id=get_language()).values('pk',
                                                                                              'question_id',
                                                                                              'text',
                                                                                              'correct_variant',
                                                                                              'variant2',
                                                                                              'variant3',
                                                                                              'variant4',
                                                                                              ).order_by('question_id')

        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'student_saved_question_list': student_saved_question_list,
            'question_text_list': question_text_list
        }

from datetime import timedelta
from django.core.cache import cache
from django.db.models import Count
from django.utils.timezone import now
from rest_framework.status import HTTP_201_CREATED
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, RetrieveAPIView, get_object_or_404
from django.utils.translation import get_language
from rest_framework.permissions import IsAuthenticated

from api.v1.general.utils import bubble_search
from api.v1.lessons.tasks import change_student_lesson_view_statistics
from api.v1.lessons.models import StudentLessonViewStatistics, Lesson, LessonStudent, LessonDetail
from api.v1.questions.models import StudentSavedQuestion, Question, QuestionDetail, CategoryDetail, Variant
from api.v1.lessons.permissions import OldLessonCompleted, IsOpenOrPurchased, OldLessonCompletedForQuestions
from api.v1.accounts.permissions import IsStudent
from api.v1.questions.serializers.questions import QuestionSerializer
from api.v1.lessons.serializers import (LessonRetrieveSerializer, StudentLessonViewStatisticsSerializer,
                                        LessonAnswerSerializer, LessonListSerializer)


class LessonAnswerAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsStudent, OldLessonCompletedForQuestions, IsOpenOrPurchased)
    serializer_class = LessonAnswerSerializer

    def post(self, request, *args, **kwargs):
        try:
            obj = get_object_or_404(Lesson, pk=request.data['lesson_id'])
            self.check_object_permissions(self.request, obj)
        except KeyError:
            pass
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=HTTP_201_CREATED)


class LessonStudentAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsStudent, OldLessonCompleted, IsOpenOrPurchased)
    serializer_class = LessonRetrieveSerializer
    queryset = Lesson.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        student = self.request.user
        page = str(request.build_absolute_uri())
        change_student_lesson_view_statistics.delay(student_id=student.id, lesson_id=instance.id)

        page_cache = cache.get(page)
        if page_cache:
            queryset = LessonStudent.objects.filter(lesson__chapter_id=instance.chapter_id, student=student
                                                    ).select_related('lesson')
            ctx = {
                'student': student,
                'lesson_title_list': LessonDetail.objects.filter(language=get_language(),
                                                                 lesson__chapter_id=instance.chapter_id
                                                                 ).values('lesson', 'title').order_by('lesson')
            }

            page_cache['lessons'] = LessonListSerializer(queryset, many=True, context=ctx).data
            return Response(page_cache)

        serializer = self.get_serializer(instance)
        cache.set(page, serializer.data)
        return Response(serializer.data)


class LessonAPIView(LessonStudentAPIView):
    lookup_field = 'lesson_id'
    lookup_url_kwarg = 'pk'


class StudentLessonViewStatisticsAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = StudentLessonViewStatisticsSerializer

    def get_queryset(self):
        return StudentLessonViewStatistics.objects.filter(student=self.request.user).values(
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
    permission_classes = (IsAuthenticated, IsStudent, OldLessonCompletedForQuestions, IsOpenOrPurchased)
    serializer_class = QuestionSerializer
    queryset = Lesson.objects.all()

    def get(self, request, *args, **kwargs):
        self.get_object()

        page = str(request.build_absolute_uri())
        page_cache = cache.get(page)
        if page_cache:
            sort_list = StudentSavedQuestion.objects.filter(student=self.request.user).values('question'
                                                                                              ).order_by('question_id')
            for i in page_cache:
                obj = bubble_search(i['id'], 'question', sort_list)
                i['is_saved'] = True if obj is not None else False
            return Response(page_cache)

        questions = Question.objects.filter(lesson_id=self.kwargs[self.lookup_field])
        serializer = self.get_serializer(questions, many=True)
        cache.set(page, serializer.data)
        return Response(serializer.data)

    def get_serializer_context(self):
        student_saved_question_list = StudentSavedQuestion.objects.filter(student=self.request.user).values(
            'question').order_by('question_id')
        question_text_list = QuestionDetail.objects.filter(language=get_language()).values('question', 'text').order_by(
            'question_id')
        category_name_list = CategoryDetail.objects.filter(language=get_language()).values('category', 'name').order_by(
            'category_id')
        variant_list = Variant.objects.filter(language=get_language(),
                                              question__lesson_id=self.kwargs[self.lookup_field]
                                              ).values('question', 'text', 'is_correct')
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'student_saved_question_list': student_saved_question_list,
            'question_text_list': question_text_list,
            'category_name_list': category_name_list,
            'variant_list': variant_list
        }

from django.conf import settings
from rest_framework.status import HTTP_201_CREATED
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from api.v1.exams.models import CategoryExamStudent
from api.v1.questions.models import StudentWrongAnswer, StudentSavedQuestion
from api.v1.accounts.permissions import IsStudent
from api.v1.accounts.serializers import ProfileExamSerializer
from api.v1.exams.serializers.categories import CategorySerializer


class ExamAnswerAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsStudent)  # last

    def post(self, request, *args, **kwargs):
        student = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = {'ball': student.ball, 'level_id': student.level_id, 'level_percent': student.level_percent}
        return Response(data, status=HTTP_201_CREATED)


class CategoryResultAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = CategorySerializer
    queryset = settings.QUESTION_CATEGORIES

    def get_serializer_context(self):
        ctx = super().get_serializer_context()

        ctx['category_exam_student_list'] = CategoryExamStudent.objects.filter(student_id=self.request.user.pk
                                                                               ).values('category_id',
                                                                                        'questions',
                                                                                        'percent').order_by('-pk')
        return ctx

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        student = self.request.user
        other_wrong_answers_count = StudentWrongAnswer.objects.exclude(student_id=student.pk).count()
        data = {
            'user': ProfileExamSerializer(student).data,
            'student_wrong_answers_count': StudentWrongAnswer.objects.filter(student_id=student.pk).count(),
            'student_saved_answers_count': StudentSavedQuestion.objects.filter(student_id=student.pk).count(),
            'other_wrong_answers_count': other_wrong_answers_count if other_wrong_answers_count <= settings.MAX_QUESTIONS else settings.MAX_QUESTIONS,
            'category_questions_count': settings.MAX_CATEGORY_QUESTIONS,
            'categories': serializer.data
        }
        return Response(data)

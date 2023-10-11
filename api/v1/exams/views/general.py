from django.utils.translation import get_language
from rest_framework.status import HTTP_201_CREATED
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from api.v1.exams.models import CategoryExamStudentResult
from api.v1.exams.serializers.categories import CategoryExamStudentResultSerializer
from api.v1.questions.models import StudentWrongAnswer, CategoryDetail, StudentSavedQuestion
from api.v1.accounts.permissions import IsStudent


class ExamAnswerAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsStudent)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=HTTP_201_CREATED)


class ExamStudentResult(GenericAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = CategoryExamStudentResultSerializer

    def get_queryset(self):
        return CategoryExamStudentResult.objects.filter(
            student=self.request.user).select_related('category').prefetch_related('categoryexamstudent_set')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()

        ctx['category_name_list'] = CategoryDetail.objects.filter(language=get_language()
                                                                  ).values('category', 'name').order_by('category_id')
        return ctx

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)

        data = {
            'all_wrong_answers_count': StudentWrongAnswer.objects.count(),
            'wrong_answers_count': StudentWrongAnswer.objects.filter(student=self.request.user).count(),
            'saved_answers_count': StudentSavedQuestion.objects.filter(student=self.request.user).count(),
            'all_saved_answers_count': StudentSavedQuestion.objects.count(),
            'category_exams': serializer.data
        }
        return Response(data)

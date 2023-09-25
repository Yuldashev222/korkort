from rest_framework.status import HTTP_201_CREATED
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from api.v1.exams.models import CategoryExamStudentResult
from api.v1.exams.serializers.categories import CategoryExamStudentResultSerializer
from api.v1.questions.models import StudentWrongAnswer
from api.v1.accounts.permissions import IsStudent


class ExamAnswerAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsStudent)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=HTTP_201_CREATED)


class ExamStudentResult(GenericAPIView):
    permission_classes = (IsAuthenticated, IsStudent)

    def get(self, request, *args, **kwargs):
        student = self.request.user
        category_exam_query = CategoryExamStudentResult.objects.filter(
            student=student).select_related('category').prefetch_related('categoryexamstudent_set')

        category_exams = CategoryExamStudentResultSerializer(category_exam_query, many=True,
                                                             context={'request': request}).data
        data = {
            'wrong_answers_count': StudentWrongAnswer.objects.filter(student=student).count(),
            'category_exams': category_exams
        }
        return Response(data)

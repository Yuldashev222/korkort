from rest_framework.status import HTTP_201_CREATED
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.utils.translation import get_language
from rest_framework.permissions import IsAuthenticated

from api.v1.accounts.serializers import ProfileExamSerializer
from api.v1.accounts.services import get_student_level
from api.v1.exams.models import CategoryExamStudentResult
from api.v1.questions.models import StudentWrongAnswer, CategoryDetail, StudentSavedQuestion
from api.v1.accounts.permissions import IsStudent
from api.v1.exams.serializers.categories import CategoryExamStudentResultSerializer


class ExamAnswerAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsStudent)  # last

    def post(self, request, *args, **kwargs):
        student = self.request.user
        old_level_id = student.level_id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(get_student_level(student, old_level_id), status=HTTP_201_CREATED)


class ExamStudentResult(GenericAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = CategoryExamStudentResultSerializer

    def get_queryset(self):
        return CategoryExamStudentResult.objects.filter(
            student_id=self.request.user.pk
        ).select_related('category').prefetch_related('categoryexamstudent_set').order_by('category__ordering_number')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()

        ctx['category_name_list'] = CategoryDetail.objects.filter(language_id=get_language()
                                                                  ).values('category_id', 'name'
                                                                           ).order_by('category_id')
        return ctx

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        student = self.request.user

        data = {
            'user': ProfileExamSerializer(student).data,
            'student_wrong_answers_count': StudentWrongAnswer.objects.filter(student_id=student.pk).count(),
            'student_saved_answers_count': StudentSavedQuestion.objects.filter(student_id=student.pk).count(),
            'other_wrong_answers_exists': StudentWrongAnswer.objects.exclude(student_id=student.pk).exists(),  # last
            'categories': serializer.data
        }
        return Response(data)

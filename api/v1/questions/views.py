from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from api.v1.questions.models import StudentSavedQuestion
from api.v1.accounts.permissions import IsStudent
from api.v1.questions.serializers.saved import StudentSavedQuestionSerializer


class StudentSavedQuestionAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = StudentSavedQuestionSerializer

    def perform_create(self, serializer):
        student = self.request.user
        question_id = serializer.validated_data['pk']
        obj, created = StudentSavedQuestion.objects.get_or_create(student=student, question_id=question_id)
        if not created:
            obj.delete()

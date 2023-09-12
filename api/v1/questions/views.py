from rest_framework.status import HTTP_201_CREATED
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from api.v1.accounts.permissions import IsStudent
from api.v1.questions.serializers.saved import SavedQuestionListCreateSerializer, SavedQuestionListDeleteSerializer


class SavedQuestionStudentAPIVIew(CreateAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = SavedQuestionListCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({}, status=HTTP_201_CREATED)


class SavedQuestionStudentDestroyAPIVIew(SavedQuestionStudentAPIVIew):
    serializer_class = SavedQuestionListDeleteSerializer

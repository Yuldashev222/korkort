from rest_framework.status import HTTP_201_CREATED
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from api.v1.exams.serializers.categories import CategoryExamAnswerSerializer, CategoryExamCreateSerializer
from api.v1.exams.serializers.general import QuestionExamSerializer
from api.v1.questions.models import Question
from api.v1.exams.views.general import ExamAnswerAPIView
from api.v1.accounts.permissions import IsStudent


class CategoryExamAnswerAPIView(ExamAnswerAPIView):
    serializer_class = CategoryExamAnswerSerializer


class CategoryExamAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = CategoryExamCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        obj = serializer.obj
        category_id = request.data['category_id']
        difficulty_level = request.data.get('difficulty_level')
        filter_data = {'category_id': category_id}
        if difficulty_level:
            filter_data['difficulty_level'] = difficulty_level

        questions_queryset = Question.objects.filter(**filter_data).prefetch_related('variant_set'
                                                                                     ).order_by('?')[:obj.questions]

        questions = QuestionExamSerializer(questions_queryset, many=True, context={'request': request}).data
        return Response({'exam_id': obj.id, 'questions': questions}, status=HTTP_201_CREATED)

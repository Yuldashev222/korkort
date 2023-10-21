from rest_framework.generics import ListAPIView, CreateAPIView
from django.utils.translation import get_language
from rest_framework.permissions import IsAuthenticated

from api.v1.accounts.permissions import IsStudent
from api.v1.general.paginations import CustomPageNumberPagination
from api.v1.todos.models import Todo, TodoDetail, TodoStudent
from api.v1.todos.serializers import TodoListSerializer, TodoStudentSerializer


class TodoListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated, IsStudent)  # last
    pagination_class = CustomPageNumberPagination
    queryset = Todo.objects.order_by('ordering_number')
    serializer_class = TodoListSerializer

    def get_queryset(self):
        language = get_language()
        return TodoDetail.objects.filter(language_id=language).values('todo_id', 'title', 'text'
                                                                      ).order_by('todo__ordering_number')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['student_todo_list'] = TodoStudent.objects.filter(student_id=self.request.user.id
                                                              ).values('todo_id', 'is_completed'
                                                                       ).order_by('todo__ordering_number')
        return ctx


class TodoStudentAPIView(CreateAPIView):
    queryset = TodoStudent.objects.all()
    serializer_class = TodoStudentSerializer

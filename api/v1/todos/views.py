from django.conf import settings
from django.utils.decorators import method_decorator
from rest_framework.generics import ListAPIView, CreateAPIView
from django.utils.translation import get_language
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.cache import cache_page

from api.v1.todos.models import Todo, TodoDetail, TodoStudent
from api.v1.todos.serializers import TodoListSerializer, TodoStudentSerializer
from api.v1.general.paginations import CustomPageNumberPagination
from api.v1.accounts.permissions import IsStudent


class TodoListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    pagination_class = CustomPageNumberPagination
    queryset = Todo.objects.order_by('ordering_number')
    serializer_class = TodoListSerializer

    @method_decorator(cache_page(settings.CACHES['default']['TIMEOUT']))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

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
    serializer_class = TodoStudentSerializer

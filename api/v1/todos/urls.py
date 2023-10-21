from django.urls import path

from .views import TodoListAPIView, TodoStudentAPIView

urlpatterns = [
    path('', TodoListAPIView.as_view(), name='todo-list'),
    path('completed/', TodoStudentAPIView.as_view(), name='todo-student')
]

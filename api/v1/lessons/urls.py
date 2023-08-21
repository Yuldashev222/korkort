from django.urls import path

from .views import LessonAPIView

urlpatterns = [
    path('', LessonAPIView.as_view({'get': 'list'})),
    path('<int:pk>/', LessonAPIView.as_view({'get': 'retrieve'})),
]

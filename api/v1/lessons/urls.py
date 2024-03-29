from django.urls import path

from api.v1.lessons import views

urlpatterns = [
    path('<int:pk>/', views.LessonAPIView.as_view()),
    path('<int:pk>/questions/', views.LessonQuestionAPIView.as_view()),
    path('statistics/', views.StudentLessonViewStatisticsAPIView.as_view()),
    path('http-live-stream/', views.HTTPLiveStream.as_view()),
    path('questions/answers/', views.LessonAnswerAPIView.as_view())
]

from celery import shared_task
from datetime import timedelta
from django.utils.timezone import now

from api.v1.lessons.models import StudentLessonViewStatistics


@shared_task
def change_student_lesson_view_statistics(lesson_id, student_id):
    StudentLessonViewStatistics.objects.filter(viewed_date__lt=now().date() - timedelta(days=7)).delete()
    StudentLessonViewStatistics.objects.get_or_create(lesson_id=lesson_id, student_id=student_id,
                                                      viewed_date=now().date())

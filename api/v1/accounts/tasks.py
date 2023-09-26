from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now

from api.v1.accounts.services import delete_not_confirmed_accounts
from api.v1.exams.models import CategoryExamStudentResult
from api.v1.lessons.models import Lesson, LessonStudent, StudentLessonViewStatistics
from api.v1.chapters.models import Chapter, ChapterStudent
from api.v1.questions.models import Category


@shared_task
def create_objects_for_student(student_id):
    objs = [ChapterStudent(chapter=chapter, student_id=student_id) for chapter in Chapter.objects.all()]
    objs[0].is_open = True
    ChapterStudent.objects.bulk_create(objs)

    lesson_ids = Lesson.objects.values_list('id', flat=True)
    objs = (LessonStudent(lesson_id=lesson_id, student_id=student_id) for lesson_id in lesson_ids)
    LessonStudent.objects.bulk_create(objs)

    objs = [CategoryExamStudentResult(category=category, student_id=student_id) for category in Category.objects.all()]
    CategoryExamStudentResult.objects.bulk_create(objs)

    delete_not_confirmed_accounts()

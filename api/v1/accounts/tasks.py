from datetime import timedelta

from celery import shared_task
from django.core.cache import cache
from django.utils.timezone import now

from api.v1.exams.models import CategoryExamStudent, CategoryExamStudentResult
from api.v1.lessons.models import Lesson, LessonStudent, LessonStudentStatisticsByDay
from api.v1.accounts.models import CustomUser
from api.v1.chapters.models import Chapter, ChapterStudent
from api.v1.questions.models import Question, StudentWrongAnswer, Category


@shared_task
def delete_not_confirmed_accounts():
    CustomUser.objects.filter(date_joined__lte=now() - timedelta(minutes=30), is_verified=False).delete()


@shared_task
def create_objects_for_student(student_id):
    lesson_ids = Lesson.objects.values_list('id', flat=True)
    objs = (LessonStudent(lesson_id=lesson_id, student_id=student_id) for lesson_id in lesson_ids)
    LessonStudent.objects.bulk_create(objs)

    objs = [
        ChapterStudent(last_lesson=LessonStudent.objects.filter(lesson__chapter=chapter, student_id=student_id).first(),
                       chapter=chapter, student_id=student_id)
        for chapter in Chapter.objects.all()
    ]
    objs[0].is_open = True
    ChapterStudent.objects.bulk_create(objs)

    today_date = now().date()
    objs = (
        LessonStudentStatisticsByDay(student_id=student_id, date=today_date - timedelta(days=i))
        for i in [0, 1, 2, 3, 4, 5, 6]
    )
    LessonStudentStatisticsByDay.objects.bulk_create(objs)

    objs = [
        CategoryExamStudentResult(category=category, student_id=student_id)
        for category in Category.objects.all()
    ]
    CategoryExamStudentResult.objects.bulk_create(objs)


@shared_task
def update_student_correct_answers(student_id):
    all_questions_count = cache.get('all_questions_count')
    if not all_questions_count:
        Question.set_redis()
        all_questions_count = cache.get('all_questions_count')

    student = CustomUser.objects.get(id=student_id)

    if all_questions_count:
        wrong_answers_count = StudentWrongAnswer.objects.filter(student=student).count()
        student.correct_answers = all_questions_count - wrong_answers_count
    else:
        student.correct_answers = 0
    student.save()

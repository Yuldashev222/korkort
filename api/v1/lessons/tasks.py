from uuid import uuid4

from celery import shared_task
from django.db.models import Max
from django.utils.timezone import now

from api.v1.accounts.models import CustomUser
from api.v1.chapters.models import Chapter
from api.v1.lessons.models import LessonStudent, LessonStudentStatistics, Lesson, LessonWordInfo, LessonSource
from api.v1.payments.models import Order


@shared_task
def delete_expire_orders():
    Order.expire_orders().delete()


@shared_task
def change_student_tariff_expire_date(student_id):
    try:
        student = CustomUser.objects.get(id=student_id)
    except CustomUser.DoesNotExist:
        return

    max_expire_at = Order.objects.filter(is_paid=True, expire_at__gt=now()
                                         ).aggregate(max_expire_at=Max('expire_at'))['max_expire_at']

    if max_expire_at:
        student.tariff_expire_date = max_expire_at
    student.save()


@shared_task
def change_student_lesson_view_statistics(lesson_id, student_id):
    LessonStudentStatistics.objects.get_or_create(lesson_id=lesson_id, student_id=student_id)


@shared_task
def create_lessons():
    chapters = Chapter.objects.order_by('-id')
    for chapter in chapters:
        print(chapter.id)
        for i in range(15):
            is_open = True if i <= 10 else False
            lesson = Lesson.objects.create(
                chapter=chapter,
                is_open=is_open,
                ordering_number=i,
                image='Screenshot_from_2023-08-17_20-41-00_7fU76Z8.png',
                title_swe=f'{uuid4()} {uuid4()} {uuid4()}',
                title_en=f'{uuid4()} {uuid4()} {uuid4()}',
                title_e_swe=f'{uuid4()} {uuid4()} {uuid4()}',
                text_swe=f'{uuid4()} {uuid4()} {uuid4()}' * i,
                text_en=f'{uuid4()} {uuid4()} {uuid4()}' * i,
                text_e_swe=f'{uuid4()} {uuid4()} {uuid4()}' * i,
                video_swe='99.mp4',
                video_en='99.mp4',
                video_e_swe='99.mp4'
            )

            for j in range(10):
                obj = LessonWordInfo.objects.create(text_swe=f'{uuid4()} {uuid4()}',
                                                    text_en=f'{uuid4()} {uuid4()}',
                                                    text_e_swe=f'{uuid4()} {uuid4()}',
                                                    info_swe=f'{uuid4()} {uuid4()} {uuid4()} {uuid4()}',
                                                    info_en=f'{uuid4()} {uuid4()} {uuid4()} {uuid4()}',
                                                    info_e_swe=f'{uuid4()} {uuid4()} {uuid4()} {uuid4()}')
                obj.lessons.set([lesson])

                obj = LessonSource.objects.create(text_swe=f'{uuid4()} {uuid4()}',
                                                  text_en=f'{uuid4()} {uuid4()}',
                                                  text_e_swe=f'{uuid4()} {uuid4()}',
                                                  link='https://google.com')
                obj.lessons.set([lesson])

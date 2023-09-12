from uuid import uuid4

from django.core.management.base import BaseCommand

from api.v1.chapters.models import Chapter
from api.v1.lessons.models import Lesson, LessonWordInfo, LessonSource


class Command(BaseCommand):
    def handle(self, *args, **options):
        chapters = Chapter.objects.order_by('-id')
        for chapter in chapters:
            self.stdout.write(str(chapter.id))
            for i in range(15):
                is_open = True if i <= 4 and chapter.ordering_number == 1 else False
                lesson = Lesson.objects.create(chapter=chapter,
                                               is_open=is_open,
                                               ordering_number=i + 1,
                                               image='discounts/images/IMG.png',
                                               title_swe=str(uuid4()),
                                               title_en=str(uuid4()),
                                               title_e_swe=str(uuid4()),
                                               text_swe=str(uuid4()) * i,
                                               text_en=str(uuid4()) * i,
                                               text_e_swe=str(uuid4()) * i,
                                               video_swe='chapters/1%3A%20836c4b38-fe8e-4ef2-9a9c-bab/lessons/1%3A%20614101a6-4c87-4dbc-9629-23a/videos/a.mp4',
                                               video_en='chapters/1%3A%20836c4b38-fe8e-4ef2-9a9c-bab/lessons/1%3A%20614101a6-4c87-4dbc-9629-23a/videos/a.mp4',
                                               video_e_swe='chapters/1%3A%20836c4b38-fe8e-4ef2-9a9c-bab/lessons/1%3A%20614101a6-4c87-4dbc-9629-23a/videos/a.mp4',
                                               lesson_time=i * 2)

                for j in range(10):
                    LessonWordInfo.objects.create(text_swe=f'{str(uuid4())[:8]}',
                                                  text_en=f'{str(uuid4())[:8]}',
                                                  text_e_swe=f'{str(uuid4())[:8]}',
                                                  info_swe=f'{uuid4()} {uuid4()} {uuid4()} {uuid4()}',
                                                  info_en=f'{uuid4()} {uuid4()} {uuid4()} {uuid4()}',
                                                  info_e_swe=f'{uuid4()} {uuid4()} {uuid4()} {uuid4()}',
                                                  lesson=lesson)

                    LessonSource.objects.create(text_swe=f'{uuid4()}' * j,
                                                text_en=f'{uuid4()}' * j,
                                                text_e_swe=f'{uuid4()}' * j,
                                                link='https://google.com',
                                                lesson=lesson)

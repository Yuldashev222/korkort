from django.core.management.base import BaseCommand

from api.v1.chapters.models import Chapter
from api.v1.general.enums import title, desc
from api.v1.languages.models import Language
from api.v1.lessons.models import Lesson, LessonWordInfo, LessonSource, LessonDetail


class Command(BaseCommand):
    def handle(self, *args, **options):
        lst1 = []
        lst2 = []
        chapters = Chapter.objects.order_by('-ordering_number')
        for chapter in chapters:
            self.stdout.write(str(chapter.pk))
            for i in range(10):
                is_open = True if i <= 4 and chapter.ordering_number == 1 else False
                lesson = Lesson.objects.create(chapter_id=chapter.pk, is_open=is_open, ordering_number=i + 1,
                                               lesson_time=i * 2,
                                               image='chapters/1:_5663e70a-0c7b-4118-907a-be4/images/Rectangle_625.png')

                for language in Language.objects.all():
                    lesson_detail = LessonDetail.objects.create(lesson_id=lesson.pk, language_id=language.pk,
                                                                title=title, text=desc, video='d.mp4')
                    for j in range(10):
                        lst1.append(LessonWordInfo(lesson_detail_id=lesson_detail.pk, word=title, info=desc))
                        lst2.append(LessonSource(lesson_detail_id=lesson_detail.pk, text=title,
                                                 link='https://offentligabeslut.se/sokmotor/'))
        LessonWordInfo.objects.bulk_create(lst1)
        LessonSource.objects.bulk_create(lst2)

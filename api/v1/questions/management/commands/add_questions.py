from uuid import uuid4
from random import randint

from django.conf import settings

from api.v1.general.enums import title, desc
from api.v1.lessons.models import Lesson
from api.v1.languages.models import Language
from api.v1.questions.models import Question, QuestionDetail
from django.core.management.base import BaseCommand


def create_questions(self, for_lesson=False):
    categories = settings.QUESTION_CATEGORIES
    lst = []

    def wrapper(lesson=None):
        ordering_number = randint(10000, 999999) if lesson else 0
        obj = Question.objects.create(lesson=lesson, category_id=category[0], ordering_number=ordering_number,
                                      video='a.mp4', difficulty_level=difficulty_level,
                                      image='chapters/1:_5663e70a-0c7b-4118-907a-be4/images/Rectangle_625.png')

        for language in Language.objects.all():
            lst.append(QuestionDetail(question_id=obj.pk, language_id=language.pk, text=str(uuid4()),
                                      correct_variant=title + ' asdasd',
                                      variant2=title,
                                      variant3=title,
                                      variant4=title,
                                      answer=desc))

    for idx, category in enumerate(categories, 1):
        self.stdout.write(str(category[0]))

        if idx > 7:
            difficulty_level = Question.DIFFICULTY_LEVEL[2][0]
        elif idx % 2 == 0:
            difficulty_level = Question.DIFFICULTY_LEVEL[0][0]
        else:
            difficulty_level = Question.DIFFICULTY_LEVEL[1][0]

        for i in range(100):
            wrapper()

        for lesson in Lesson.objects.all():
            for i in range(2):
                wrapper(lesson=lesson)

    QuestionDetail.objects.bulk_create(lst)
    Question.set_redis()


class Command(BaseCommand):
    def handle(self, *args, **options):
        create_questions(self)
